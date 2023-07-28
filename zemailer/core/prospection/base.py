import asyncio
import dataclasses
import datetime
import itertools
import json
import logging
import secrets
import string
import time
from dataclasses import dataclass, field
from functools import cached_property

import pytz


class BaseModel:
    @cached_property
    def fields(self):
        fields = dataclasses.fields(self)
        return list(map(lambda x: x.name, fields))

    def as_json(self):
        return_value = {}
        for field in self.fields:
            return_value[field] = getattr(self, field)
        return return_value


@dataclass
class Step(BaseModel):
    date_sent: str
    id: str = None
    template: str = None
    date_sent: str = None
    days_before_send: str = None
    next_date: str = None
    active: bool = False
    completed: bool = False
    email_state: dict = field(default_factory=dict)
    category: int = field(default=1)

    def __post_init__(self):
        self._for_email = None
        self.email_state = {
            'sent': False,
            'bounced': False,
            'opened': False,
            'clicked': False
        }

        if self.category == 1 and not self.active:
            self.active = True

        if self.id is None:
            self.id = self.create_step_id

    def __repr__(self):
        return f'<Step {self.category}, active={self.active}, completed={self.completed}>'

    def __hash__(self):
        return hash([self.id, self._for_email, self.category])

    @property
    def create_step_id(self):
        return secrets.token_hex(10)

    @property
    def can_be_completed(self):
        return all([self.active, not self.completed])

    def prepare(self, email, start_date):
        self._for_email = email
        next_date = start_date + datetime.timedelta(days=self.days_before_send)
        self.next_date = str(next_date)

    def transform_date(self, d):
        return datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f%z')

    def send(self):
        timezone = pytz.timezone('UTC')
        current_date = datetime.datetime.now(tz=timezone)
        next_date = self.transform_date(self.next_date)
        if next_date.date() == current_date.date():
            self.date_sent = str(current_date)
            self.active = False
            self.completed = True
            self.email_state['sent'] = True

        print('Sending step', self.category, 'to', self._for_email)


@dataclass
class Email(BaseModel):
    first_name: str
    last_name: str
    email: str
    current_step: int = field(default=1)
    completed: bool = False
    steps: list = field(default_factory=list)

    def __post_init__(self):
        timezone = pytz.timezone('UTC')
        current_date = datetime.datetime.now(tz=timezone)
        self._start_date = current_date
        errors = []
        steps = []
        seen_step = []
        step_states = []
        for step in self.steps:
            category = step['category']
            if category in seen_step:
                errors.append(Exception('Step exists already'))
            seen_step.append(category)
            step_states.append(step['active'])

        if all(step_states):
            errors.append(
                Exception('Only one step should be active at a time'))

        if errors:
            raise ExceptionGroup(
                'Problem with steps',
                errors
            )

        for step in self.steps:
            step_object = Step(**step)
            step_object.prepare(self.email, self._start_date)
            steps.append(step_object)
        self.steps = steps

    def __repr__(self):
        return f'<Email {self.email}>'

    def __hash__(self):
        return hash((self.email))

    @property
    def get_current_step(self):
        if self.current_step > self.number_of_steps:
            return False
        return self.steps[self.current_step - 1]

    @property
    def get_next_step(self):
        next_step = self.current_step + 1
        if next_step > self.number_of_steps:
            return False
        return self.steps[next_step - 1]

    @property
    def number_of_steps(self):
        return len(self.steps)

    @property
    def has_next_step(self):
        current_index = self.steps.index(self.current_step)
        next_index = current_index + 1
        return next_index + 1 >= self.number_of_steps

    def create_step(self, data):
        step = Step(**data)
        self.steps.append(step)

    def as_json(self):
        return_value = {}
        for field in self.fields:
            value = getattr(self, field)
            if field == 'steps':
                value = list(map(lambda x: x.as_json(), value))
            return_value[field] = value
        return return_value

    def evaluate(self):
        steps = []
        for step in self.steps:
            if step.can_be_completed:
                # steps.append((step, self.get_next_step))
                steps.append(step)
        return steps


# with open('zemailer/core/prospection/prospects.json', mode='r') as f:
#     data = json.load(f)
#     e = Email(**data[0])
#     e.complete_current_step()
#     print(e)


class EmailBroker:
    current_date = None
    emails = []
    _cache = []

    def __init__(self):
        self.emails_to_send = []

    def load_steps_to_execute(self):
        """Load the emails to send for the day"""
        emails = [email for email in self.emails]
        self.emails_to_send = emails
        for email in emails:
            yield email.evaluate()

    def load_file(self):
        with open('zemailer/core/prospection/prospects.json', mode='r', encoding='utf-8') as f:
            data = json.load(f)
            print(len(data['items']))
            timezone = pytz.timezone('UTC')
            self.current_date = datetime.datetime.now(tz=timezone)
            if data['start_date'] is None:
                data['start_date'] = str(self.current_date)

            self._cache = data

            def initialize_email(data):
                return Email(**data)

            self.emails = list(map(initialize_email, data['items']))
            print('loaded file')

    def update_file(self):
        with open('zemailer/core/prospection/prospects.json', mode='w', encoding='utf-8') as f:
            data = [email.as_json() for email in self.emails]
            self._cache['items'] = data
            json.dump(self._cache, f, indent=4, sort_keys=True)
            time.sleep(3)


# broker = EmailBroker()
# broker.load_file()
# broker
# print(broker._cache)


async def main():
    broker = EmailBroker()
    broker.current_date = datetime.datetime.now()

    steps_queue = asyncio.Queue()

    async def email_sender():
        while True:
            if not steps_queue.empty():
                # step, next_step = await steps_queue.get()
                step = await steps_queue.get()
                step.send()
                # next_step.active = True
                broker.update_file()
                await steps_queue.join()

            await asyncio.sleep(1)

    async def email_loader():
        while True:
            broker.load_file()
            steps = broker.load_steps_to_execute()
            list_of_steps = list(itertools.chain(*steps))
            for step in list_of_steps:
                await steps_queue.put(step)
            await asyncio.sleep(5)

    await asyncio.gather(email_loader(), email_sender())


if __name__ == '__main__':
    asyncio.run(main())
