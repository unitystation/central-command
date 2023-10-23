from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from ..models import Other, PolyPhrase
from ..api.views import 

class OtherModelTestCase(TestCase):
    """Test case for the Other model."""

    def setUp(self):
        """Set up the test case."""
        self.client = APIClient()
        self.other = Other.objects.create(account='test_account', other_data={'key': 'value'})
        self.polyphrase = PolyPhrase.objects.create(said_by='test_speaker', phrase='test_phrase')

    def test_create_other(self):
        """Test the creation of an Other instance."""
        response = self.client.post(reverse('other-list'), {'account': 'new_account', 'other_data': {'new_key': 'new_value'}}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Other.objects.count(), 2)
        self.assertEqual(Other.objects.get(account='new_account').other_data, {'new_key': 'new_value'})

    def test_read_other(self):
        """Test the reading of an Other instance."""
        response = self.client.get(reverse('other-detail', kwargs={'pk': self.other.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'account': 'test_account', 'other_data': {'key': 'value'}})

    def test_update_other(self):
        """Test the updating of an Other instance."""
        response = self.client.put(reverse('other-detail', kwargs={'pk': self.other.pk}), {'account': 'test_account', 'other_data': {'updated_key': 'updated_value'}}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Other.objects.get(account='test_account').other_data, {'updated_key': 'updated_value'})

    def test_delete_other(self):
        """Test the deletion of an Other instance."""
        response = self.client.delete(reverse('other-detail', kwargs={'pk': self.other.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Other.objects.count(), 0)

class PolyPhraseModelTestCase(TestCase):
    """Test case for the PolyPhrase model."""

    def setUp(self):
        """Set up the test case."""
        self.client = APIClient()
        self.polyphrase = PolyPhrase.objects.create(said_by='test_speaker', phrase='test_phrase')

    def test_create_polyphrase(self):
        """Test the creation of a PolyPhrase instance."""
        response = self.client.post(reverse('polyphrase-list'), {'said_by': 'new_speaker', 'phrase': 'new_phrase'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PolyPhrase.objects.count(), 2)
        self.assertEqual(PolyPhrase.objects.get(said_by='new_speaker').phrase, 'new_phrase')

    def test_read_polyphrase(self):
        """Test the reading of a PolyPhrase instance."""
        response = self.client.get(reverse('polyphrase-detail', kwargs={'pk': self.polyphrase.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'said_by': 'test_speaker', 'phrase': 'test_phrase'})

    def test_update_polyphrase(self):
        """Test the updating of a PolyPhrase instance."""
        response = self.client.put(reverse('polyphrase-detail', kwargs={'pk': self.polyphrase.pk}), {'said_by': 'updated_speaker', 'phrase': 'updated_phrase'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PolyPhrase.objects.get(said_by='updated_speaker').phrase, 'updated_phrase')

    def test_delete_polyphrase(self):
        """Test the deletion of a PolyPhrase instance."""
        response = self.client.delete(reverse('polyphrase-detail', kwargs={'pk': self.polyphrase.pk}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(PolyPhrase.objects.count(), 0)

class ReadOtherDataViewTestCase(TestCase):
    """Test case for the ReadOtherDataView."""

    def setUp(self):
        """Set up the test case."""
        self.client = APIClient()
        self.other = Other.objects.create(account='test_account', other_data={'key': 'value'})

    def test_get_request(self):
        """Test a GET request to the ReadOtherDataView."""
        response = self.client.get(reverse('read-other-data', kwargs={'pk': self.other.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'account': 'test_account', 'other_data': {'key': 'value'}})

class WriteOtherDataViewTestCase(TestCase):
    """Test case for the WriteOtherDataView."""

    def setUp(self):
        """Set up the test case."""
        self.client = APIClient()
        self.other = Other.objects.create(account='test_account', other_data={'key': 'value'})

    def test_post_request(self):
        """Test a POST request to the WriteOtherDataView."""
        response = self.client.post(reverse('write-other-data', kwargs={'pk': self.other.pk}), {'account': 'test_account', 'other_data': {'updated_key': 'updated_value'}}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Other.objects.get(account='test_account').other_data, {'updated_key': 'updated_value'})

class RandomPolyPhraseViewTestCase(TestCase):
    """Test case for the RandomPolyPhraseView."""

    def setUp(self):
        """Set up the test case."""
        self.client = APIClient()
        self.polyphrase = PolyPhrase.objects.create(said_by='test_speaker', phrase='test_phrase')

    def test_get_request(self):
        """Test a GET request to the RandomPolyPhraseView."""
        response = self.client.get(reverse('random-polyphrase'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'said_by': 'test_speaker', 'phrase': 'test_phrase'})

class WritePolyPhraseViewTestCase(TestCase):
    """Test case for the WritePolyPhraseView."""

    def setUp(self):
        """Set up the test case."""
        self.client = APIClient()
        self.polyphrase = PolyPhrase.objects.create(said_by='test_speaker', phrase='test_phrase')

    def test_post_request(self):
        """Test a POST request to the WritePolyPhraseView."""
        response = self.client.post(reverse('write-polyphrase'), {'said_by': 'new_speaker', 'phrase': 'new_phrase'}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(PolyPhrase.objects.count(), 2)
        self.assertEqual(PolyPhrase.objects.get(said_by='new_speaker').phrase, 'new_phrase')
