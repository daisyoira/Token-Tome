from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from token_tome.models import Student
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import LiveServerTestCase
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from faker import Faker


class StudentTestsWithAuth(APITestCase):

    def setUp(self):
        self.username = 'daisy'
        self.password = 'daisy-secret'
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.client.login(username=self.username,
                          password=self.password)
    def test_create_student(self):
        """
        Ensure we can create a new student object.
        """

        url = reverse('student-list')
        data = {'name': 'Test Student'}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().name, 'Test Student')

    def test_create_student_missing_fields(self):
        """
        Ensure we can create a new student object.
        """

        url = reverse('student-list')
        data = {}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_existing_student(self):
        """
        Ensure we can get a student record.
        """
        student = Student.objects.create(name='JAMES')

        url = reverse('student-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({"name": response.data["name"]},
                         { "name": "JAMES"})
    def test_get_non_existing_student(self):
        """
        Ensure we can't retrieve a non-existing
        student record.
        """

        url = reverse('student-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class StudentTestsWithoutAuth(APITestCase):

    def test_create_student(self):
        """
        Ensure we can't create a new student object.
        """

        url = reverse('student-list')
        data = {'name': 'Test Student'}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Student.objects.count(), 0)

    def test_create_student_missing_fields(self):
        """
        Ensure we can't create a new student object.
        """

        url = reverse('student-list')
        data = {}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_existing_student(self):
        """
        Ensure we can't get a student record.
        """
        student = Student.objects.create(name='JAMES')

        url = reverse('student-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_non_existing_student(self):
        """
        Ensure we can't retrieve a non-existing
        student record.
        """

        url = reverse('student-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



class FileUploadWithAuth(APITestCase):

    def setUp(self):
        self.username = 'daisy'
        self.password = 'daisy-secret'
        self.user = User.objects.create_user(username=self.username,
                                             password=self.password)
        self.client.login(username=self.username,
                          password=self.password)

    def test_upload_file_missing_file(self):
        """
        Ensure we can't upload a file without
        the file field
        """

        url = reverse('file_upload')
        data = {'student': 'test_token'}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_file_missing_student(self):
        """
        Ensure we can't upload a file without
        the student field.
        """

        url = reverse('file_upload')
        data = {}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_file_missing_all_fields(self):
        """
        Ensure we can't upload a file without
        the student field and the file field.
        """

        url = reverse('file_upload')
        data = {}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class FileUploadWithoutAuth(APITestCase):


    def test_upload_file_all_fields(self):
        """
        Ensure we can upload a file & token.
        """

        url = reverse('file_upload')
        local_file = SimpleUploadedFile("test_pdf.pdf",
                                        b"file_content",
                                        content_type="application/pdf")
        #local_file.save('test_pdf.pdf', File(open('test_pdf.pdf', 'rb')))
        #with open('test_pdf.pdf') as f1:
        data = {'file': local_file,
                'student': 'test_token'}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_upload_file_missing_file(self):
        """
        Ensure we can't upload a file without
        authentication
        """

        url = reverse('file_upload')
        data = {'student': 'test_token'}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_file_missing_student(self):
        """
        Ensure we can't upload a file without
        authentication
        """

        url = reverse('file_upload')
        data = {}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_file_missing_all_fields(self):
        """
        Ensure we can't upload a file without
        authentication
        """

        url = reverse('file_upload')
        data = {}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class UserInterfaceTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Edge()

    def test_create_student_link(self):
        self.driver.get("http://localhost:8000")
        self.assertIn("Token Tome", self.driver.title)
        elem = self.driver.find_element(By.LINK_TEXT, "create a new student?")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertEqual("Add a New Student", elem.text)

    def test_protect_file_link(self):
        self.driver.get("http://localhost:8000/create-student")
        self.assertIn("Token Tome", self.driver.title)
        elem = self.driver.find_element(By.LINK_TEXT, "protect a file?")
        #elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertEqual("File Upload", elem.text)

    def test_student_form_complete(self):
        self.driver.get("http://localhost:8000/create-student")
        self.assertIn("Token Tome", self.driver.title)
        elem = self.driver.find_element(By.XPATH, "//input[@name='name'][@type='text']")

        name = Faker().name()
        elem.send_keys(name)
        elem.send_keys(Keys.RETURN)
        elem = self.driver.find_element(By.TAG_NAME, "h2")
        self.assertIn(f"Hello {name}!", elem.text)

    def test_student_form_incomplete(self):
        self.driver.get("http://localhost:8000/create-student")
        self.assertIn("Token Tome", self.driver.title)
        elem = self.driver.find_element(By.XPATH, "//input[@name='name'][@type='text']")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertEqual("Add a New Student", elem.text)
        
    def test_file_form_incomplete(self):
        self.driver.get("http://localhost:8000/")
        self.assertIn("Token Tome", self.driver.title)
        elem = self.driver.find_element(By.XPATH, "//input[@type='submit'][@value='Upload']")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertEqual("File Upload", elem.text)

    def tearDown(self):
        time.sleep(10)
        self.driver.close()


