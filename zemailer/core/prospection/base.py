import asyncio
import dataclasses
import datetime
import json
import logging
import secrets
import string
import time
from dataclasses import dataclass, field
from functools import cached_property


@dataclass
class Step:
    id: str
    date_sent: str
    active: bool = False
    completed: bool = False
    category: int = field(default=1)

    def __post_init__(self):
        if self.category == 1 and not self.active:
            self.active = True

    def __repr__(self):
        return f'<Step {self.category}, active={self.active}, completed={self.completed}>'

@dataclass
class Email:
    first_name: str
    last_name: str
    email: str
    completed: bool = False
    first_sent: str = None
    email_state: dict = field(default_factory=dict)
    steps: list = field(default_factory=list)
    
    def __post_init__(self):
        self.email_state = {
            'sent': False,
            'bounced': False,
            'opened': False,
            'clicked': False
        }
        self.steps.append({
            "id": self.create_step_id,
            "category": 1,
            "date_sent": None,
            "active": False,
            "completed": False
        })

    def __repr__(self):
        return f'<Email {self.email}>'
    
    def __hash__(self):
        return hash((self.email))
    
    @property
    def create_step_id(self):
        return secrets.token_hex(10)
    
    @property
    def current_step(self):
        def only_active_step(step):
            return step['active']
        
        items = list(filter(only_active_step, self.steps))
        if len(items) > 1:
            raise

        return Step(**items[-1])
    
    @cached_property
    def fields(self):
        fields = dataclasses.fields(self)
        return list(map(lambda x: x.name, fields))
        
    def send(self):
        self.email_state['sent'] = True
        print('Sending email for', self.email)

    def as_json(self):
        return_value = {}
        for field in self.fields:
            return_value[field] = getattr(self, field)
        return return_value
    


class EmailBroker:
    current_date = None
    emails = []
    _cached_emails = []
    
    @property
    def uncompleted_emails(self):
        return list(filter(lambda x: not x.completed, self.emails))

    def load_file(self):
        with open('zemailer/core/prospection/prospects.json', mode='r', encoding='utf-8') as f:
            self._cached_data = json.load(f)
            self.emails = list(map(lambda x: Email(**x), self._cached_data))

            if self.current_date.date() != datetime.datetime.now().date():
                self.current_date = datetime.datetime.now()
            print('loaded file')

    def update_file(self):
        pass

    def load_emails_to_send(self):
        """Load the emails to send for the day"""
        emails_to_send = []
        for email in self.emails:
            if email.current_step.active and not email.current_step.completed:
                emails_to_send.append(email)
        return emails_to_send

    def send_emails(self, emails):
        """Send emails and reset the emails 
        to send for the day"""
        for email in emails:
            email.send()
        self.emails_to_send = []


async def main():
    sender = EmailBroker()
    sender.current_date = datetime.datetime.now()

    email_queue = asyncio.Queue()

    async def email_sender():
        while True:
            if not email_queue.empty():
                email = await email_queue.get()
                print('Sending', email)
                print(email_queue)
                await email_queue.join()
                
            await asyncio.sleep(1)

    async def email_loader():
        while True:
            sender.load_file()
            emails = sender.load_emails_to_send()
            if emails:
                for email in emails:
                    await email_queue.put(email)
            await asyncio.sleep(5)

    await asyncio.gather(email_loader(), email_sender())


if __name__ == '__main__':
    asyncio.run(main())
