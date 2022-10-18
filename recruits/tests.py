from rest_framework.test import APITestCase
from recruits.models import Recruit
from companies.models import Company


class TestRecruits(APITestCase):
    def setUp(self):
        self.wanted = Company.objects.create(
            name="원티드랩",
            nation="korea",
            area="서울",
        )
        self.kakao = Company.objects.create(
            name="카카오",
            nation="korea",
            area="서울",
        )
        self.wanted_recruit = Recruit.objects.create(
            position="Django 백엔드 개발자",
            reward=1000000,
            description="원티드랩에서 백엔드 주니어 개발자를 채용합니다.",
            skill="Python",
            company=self.wanted,
        )
        self.kakao_recruit = Recruit.objects.create(
            position="Django 백엔드 개발자",
            reward=500000,
            description="카카오에서 백엔드 주니어 개발자를 채용합니다.",
            skill="Django",
            company=self.kakao,
        )

    def test_all_recruits(self):
        response = self.client.get("/api/v1/recruits/")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertNotIn("description", data[0])
        self.assertEqual(data[0]["company_name"], self.wanted.name)
        self.assertEqual(data[0]["company_nation"], self.wanted.nation)
        self.assertEqual(data[0]["company_area"], self.wanted.area)
        self.assertEqual(data[0]["position"], self.wanted_recruit.position)
        self.assertEqual(data[0]["reward"], self.wanted_recruit.reward)
        self.assertEqual(data[0]["skill"], self.wanted_recruit.skill)

    def test_search_recruits(self):
        response = self.client.get("/api/v1/recruits/?search=원티드")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertNotIn("description", data[0])
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["company_name"], self.wanted.name)
        self.assertEqual(data[0]["company_nation"], self.wanted.nation)
        self.assertEqual(data[0]["company_area"], self.wanted.area)
        self.assertEqual(data[0]["position"], self.wanted_recruit.position)
        self.assertEqual(data[0]["reward"], self.wanted_recruit.reward)
        self.assertEqual(data[0]["skill"], self.wanted_recruit.skill)

        response = self.client.get("/api/v1/recruits/?search=Django")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertNotIn("description", data[0])
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["company_name"], self.wanted.name)
        self.assertEqual(data[0]["company_nation"], self.wanted.nation)
        self.assertEqual(data[0]["company_area"], self.wanted.area)
        self.assertEqual(data[0]["position"], self.wanted_recruit.position)
        self.assertEqual(data[0]["reward"], self.wanted_recruit.reward)
        self.assertEqual(data[0]["skill"], self.wanted_recruit.skill)
