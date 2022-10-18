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

    def test_create_recruits(self):
        response = self.client.post("/api/v1/recruits/")
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["detail"], "Company id is required.")

        response = self.client.post("/api/v1/recruits/", {"company_id": 3})
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["detail"], "Company not found.")

        response = self.client.post(
            "/api/v1/recruits/",
            {
                "company_id": self.wanted.id,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("position", data)
        self.assertIn("reward", data)
        self.assertIn("description", data)
        self.assertIn("skill", data)

        response = self.client.post(
            "/api/v1/recruits/",
            {
                "company_id": self.wanted.id,
                "position": "프론트엔드 주니어 개발자",
                "reward": 300000,
                "description": "프론트엔드 주니어 개발자를 모집합니다.",
                "skill": "React",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["position"], "프론트엔드 주니어 개발자")


class TestRecruit(APITestCase):
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

    def test_recruit_not_found(self):
        response = self.client.put("/api/v1/recruits/4")
        data = response.json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["detail"], "Not found.")

    def test_one_recruit(self):
        response = self.client.put("/api/v1/recruits/1")
        data = response.json()

        self.assertIn("description", data)
        self.assertEqual(data["skill"], self.wanted_recruit.skill)
        self.assertIsInstance(data, dict)

    def test_update_recruit(self):
        response = self.client.put("/api/v1/recruits/1", {"company_id": 2})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(data["company_name"], self.kakao.name)

        response = self.client.put(
            "/api/v1/recruits/1",
            {
                "skill": "Flask",
                "reward": 300000,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["skill"], "Flask")
        self.assertEqual(data["reward"], 300000)

    def test_delete_recruit(self):
        response = self.client.delete("/api/v1/recruits/1")

        self.assertEqual(response.status_code, 204)

        response = self.client.get("/api/v1/recruits/1")

        self.assertEqual(response.status_code, 404)
