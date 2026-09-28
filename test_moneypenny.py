import unittest
from datetime import datetime
from email import policy
from email.parser import BytesParser
from unittest.mock import patch
import moneypenny as m

RAW=b'Subject: Fixture\r\nFrom: client@example.com\r\nTo: owner@example.com\r\nMessage-ID: <one@example.com>\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<style>hidden</style><p>Please call Tuesday.</p>'
class FakeIMAP:
    def __init__(self,*a,**kw): self.folder=None
    def __enter__(self): return self
    def __exit__(self,*a): pass
    def login(self,*a): pass
    def list(self): return 'OK',[b'(\\HasNoChildren) "/" "INBOX"',b'(\\Sent) "/" "Sent"',b'(\\Trash) "/" "Trash"']
    def select(self,folder,readonly=False):
        assert readonly is True
        self.folder=folder
        return 'OK',[b'1']
    def uid(self,command,*args):
        assert command in ('search','fetch'),command
        if command=='search': return 'OK',[b'7']
        assert args[1]=='(BODY.PEEK[])'
        return 'OK',[(b'7 (BODY[] {100}',RAW)]

class Tests(unittest.TestCase):
    def test_dst_and_weekend(self):
        for stamp in ['2026-09-29T10:30:00+00:00','2026-12-01T11:30:00+00:00']:
            self.assertTrue(m.due(datetime.fromisoformat(stamp)))
        for stamp in ['2026-09-29T11:30:00+00:00','2026-12-01T10:30:00+00:00','2026-10-03T10:30:00+00:00']:
            self.assertFalse(m.due(datetime.fromisoformat(stamp)))
    def test_html(self):
        text=m.body_text(BytesParser(policy=policy.default).parsebytes(RAW))
        self.assertIn('Please call Tuesday.',text);self.assertNotIn('hidden',text)
    def test_readonly_and_duplicate(self):
        with patch.object(m.imaplib,'IMAP4_SSL',FakeIMAP): items,notes=m.collect('a','b',30,250)
        self.assertEqual(len(items),1)
        self.assertIn('INBOX',items[0]['source'])
    def test_folders(self):
        self.assertIsNone(m.folder_name(b'(\\Junk) "/" "Spam"'))
        self.assertEqual(m.folder_name(b'(\\HasNoChildren) "/" "Saved Mail"')[0],'"Saved Mail"')
if __name__=='__main__': unittest.main()
