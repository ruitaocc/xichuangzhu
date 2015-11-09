# coding: utf-8
from .suite import BaseSuite


class TestCollection(BaseSuite):
    def test_action(self):
        rv = self.client.get('/collection/action')
        assert rv.status_code == 200
