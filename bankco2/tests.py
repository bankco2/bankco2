from django.test import TestCase

from rest_framework.test import APIClient

# Using the standard RequestFactory API to create a form POST request
from bankco2.models import Step


class StepAPITestCase(TestCase):
    client = APIClient()

    def test_create_new_step(self):
        data = {
            'device_id': 'test_device',
            'count': 999,
            'step_date': '1992-09-16'
        }
        request = self.client.post('/api/steps/', data)

        self.assertEqual(request.data.get('device_id'), data['device_id'])
        self.assertEqual(int(request.data.get('count')), data['count'])
        self.assertEqual(request.data.get('step_date'), data['step_date'])

    def test_create_or_update_step(self):
        data = {
            'device_id': 'test_device',
            'count': 999,
            'step_date': '1992-09-16'
        }

        self.client.post('/api/steps/', data)

        data_id = Step.objects.get(device_id='test_device').pk

        # After save data, save data2
        data2 = {
            'device_id': 'test_device',
            'count': 2432,
            'step_date': '1992-09-17'
        }

        resp_data2 = self.client.post('/api/steps/', data2)
        data2_id = Step.objects.get(device_id='test_device').pk

        self.assertEqual(data_id, data2_id)
        self.assertEqual(resp_data2.data.get('count'), 2432)
        self.assertEqual(resp_data2.data.get('step_date'), '1992-09-17')

        with self.assertRaises(Step.DoesNotExist):
            count_999_obj = Step.objects.get(count=999).pk

        data3 = {
            'device_id': 'test_device2',
            'count': 352235,
            'step_date': '1992-09-18'
        }

        self.client.post('/api/steps/', data3)
        data3_id = Step.objects.get(device_id='test_device2').pk

        self.assertNotEqual(data2_id, data3_id)
