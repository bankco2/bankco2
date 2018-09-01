from django.test import TestCase

from rest_framework.test import APIClient

# Using the standard RequestFactory API to create a form POST request
from bankco2.models import Step, Device, Animal


class StepAPITestCase(TestCase):
    client = APIClient()

    def setUp(self):
        for device_id in range(5):
            Device.objects.create(device_id=device_id)

    def test_create_new_step(self):
        data = {
            'device': '1',
            'count': 999,
            'step_date': '1992-09-16'
        }
        request = self.client.post('/api/steps/', data)

        self.assertEqual(request.data.get('device'), int(data['device']))
        self.assertEqual(int(request.data.get('count')), data['count'])
        self.assertEqual(request.data.get('step_date'), data['step_date'])

    def test_create_or_update_step(self):
        data = {
            'device': '2',
            'count': 999,
            'step_date': '1992-09-16'
        }

        self.client.post('/api/steps/', data)

        data_id = Step.objects.get(device_id='2').pk

        # After save data, save data2
        data2 = {
            'device': '2',
            'count': 2432,
            'step_date': '1992-09-17'
        }

        resp_data2 = self.client.post('/api/steps/', data2)
        self.assertEqual(resp_data2.status_code, 201)
        data2_id = Step.objects.get(device_id=2).pk

        self.assertEqual(data_id, data2_id)
        self.assertEqual(resp_data2.data.get('count'), 2432)
        self.assertEqual(resp_data2.data.get('step_date'), '1992-09-17')

        with self.assertRaises(Step.DoesNotExist):
            count_999_obj = Step.objects.get(count=999).pk

        data3 = {
            'device': '4',
            'count': 352235,
            'step_date': '1992-09-18'
        }

        self.client.post('/api/steps/', data3)
        data3_id = Step.objects.get(device_id=4).pk

        self.assertNotEqual(data2_id, data3_id)


class DrawTestCase(TestCase):
    client = APIClient()

    def setUp(self):
        for device_id in range(5):
            Device.objects.create(device_id=device_id)

        names = ['호랑이', '사자', '펭귄', '고래', '물고기']

        for idx, name in enumerate(names):
            Animal.objects.create(image=str(idx), name=name)

    def test_draw_animal_image(self):
        resp = self.client.get('/drawing/1/')

        print(resp)

        self.assertIsNotNone(resp.data.get('name'))
