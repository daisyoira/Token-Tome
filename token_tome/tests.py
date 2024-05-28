from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from token_tome.models import Student, File
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from django.db import connection
from django.test import LiveServerTestCase
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from faker import Faker
import os


class StudentTestsWithAuth(APITestCase):

    def setUp(self):
        self.username = 'test'
        self.password = 'daisy-secret'
        try:
            self.user = User.objects.create_user(username=self.username,
                                                 password=self.password)
        except Exception:
            print('User already exists')

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

    def test_create_student_missing_name_field(self):
        """
        Ensure we can create a new student object.
        """

        url = reverse('student-list')
        data = {'institution': 'Test Institution'}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_create_student_missing_institution_field(self):
        """
        Ensure we can create a new student object.
        """
        fake = Faker()
        name = fake.name()
        url = reverse('student-list')
        data = {'name': name}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_existing_student(self):
        """
        Ensure we can get a student record.
        """
        fake = Faker()
        name = fake.name()
        student = Student.objects.create(name=name, institution='Test Institution')

        url = reverse('student-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({"name": response.data["name"],
                          'institution': response.data["institution"]},
                         { "name": name,
                           'institution': 'Test Institution'})
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
    def test_create_student_missing_name_field(self):
        """
        Ensure we can create a new student object.
        """

        url = reverse('student-list')
        data = {'institution': 'Test Institution'}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_create_student_missing_institution_field(self):
        """
        Ensure we can create a new student object.
        """
        fake = Faker()
        name = fake.name()
        url = reverse('student-list')
        data = {'name': name}
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_existing_student(self):
        """
        Ensure we can't get a student record.
        """
        fake = Faker()
        name = fake.name()
        student = Student.objects.create(name=name, institution='Test Institution')

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
        super().setUp()
        self.username = 'daisy'
        self.password = 'daisy-secret'
        try:

            self.user = User.objects.create_user(username=self.username,
                                                 password=self.password)
        except Exception:
            print('User already exists')

        self.client.login(username=self.username,
                          password=self.password)


    def test_upload_file_all_fields(self):
        """
        Ensure we can upload a file & token.

        url = reverse('file_upload')
        student = Student.objects.create(name='James Finn')

        student = Student.objects.get()
        print(student)

        choices = File.objects.values('student')
        print(choices)


        path = os.path.join(settings.MEDIA_ROOT,
                            'test.pdf')
        local_file = open(path, 'rb')
        # local_file.save('test_pdf.pdf', File(open('test_pdf.pdf', 'rb')))
        # with open('test_pdf.pdf') as f1:
        # SimpleUploadedFile(local_file.name, local_file.read(), content_type='application/pdf')
        #data = {"student": student.token,
        #        "file": (open(path, 'rb'))}
        #files = {"file": SimpleUploadedFile(local_file.name, local_file.read(), content_type='application/pdf')}

        #response = self.client.post(url, data)
        #print(response.data)
        #self.assertEqual(response.status_code, status.HTTP_200_OK)
        """
        pass

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
        path = os.path.join(settings.MEDIA_ROOT,
                            'test.pdf')

        url = reverse('file_upload')
        data = {'file': (open(path, 'rb'))}
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

    def tearDown(self):
        super().tearDown()
        self.client.logout()



class FileUploadWithoutAuth(APITestCase):

    def test_upload_file_all_fields(self):
        """
        Ensure we can upload a file & token.
        """

        url = reverse('file_upload')
        path = os.path.join(settings.MEDIA_ROOT,
                            'test.pdf')
        local_file = open(path, 'rb')
        data = {'file': (open(path, 'rb')),
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
        self.assertIn("LibID", self.driver.title)
        elem = self.driver.find_element(By.LINK_TEXT, "create a new student?")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertEqual("Add a New Student", elem.text)

    def test_protect_file_link(self):
        self.driver.get("http://localhost:8000/create-student")
        self.assertIn("LibID", self.driver.title)
        elem = self.driver.find_element(By.LINK_TEXT, "protect a file?")
        #elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertEqual("File Upload", elem.text)

    def test_student_form_complete(self):
        self.driver.get("http://localhost:8000/create-student")
        self.assertIn("LibID", self.driver.title)
        elem = self.driver.find_element(By.XPATH, "//input[@name='name'][@type='text']")

        name = Faker().name()
        elem.send_keys(name)
        elem.send_keys(Keys.RETURN)
        elem = self.driver.find_element(By.TAG_NAME, "h2")
        self.assertIn(f"Hello {name}!", elem.text)

    def test_student_form_incomplete(self):
        self.driver.get("http://localhost:8000/create-student")
        self.assertIn("LibID", self.driver.title)
        elem = self.driver.find_element(By.XPATH, "//input[@name='name'][@type='text']")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertEqual("Add a New Student", elem.text)
        
    def test_file_form_incomplete(self):
        self.driver.get("http://localhost:8000/")
        self.assertIn("LibID", self.driver.title)
        elem = self.driver.find_element(By.XPATH, "//input[@type='submit'][@value='Upload']")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertEqual("File Upload", elem.text)

    def test_full_user_cycle(self):

        self.driver.get("http://localhost:8000")
        self.assertIn("LibID", self.driver.title)
        elem = self.driver.find_element(By.LINK_TEXT, "create a new student?")
        elem.send_keys(Keys.RETURN)

        time.sleep(10)

        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertEqual("Add a New Student", elem.text)

        elem = self.driver.find_element(By.XPATH, "//input[@name='name'][@type='text']")
        name = Faker().name()
        elem.send_keys(name)

        time.sleep(10)

        elem.send_keys(Keys.RETURN)
        elem = self.driver.find_element(By.TAG_NAME, "h2")
        self.assertIn(f"Hello {name}!", elem.text)


        token = self.driver.find_element(By.TAG_NAME, "span")
        elem = self.driver.find_element(By.LINK_TEXT, "protect a file?")
        elem.send_keys(Keys.RETURN)
        elem = self.driver.find_element(By.TAG_NAME, "h3")
        self.assertIn("File Upload", elem.text)

        time.sleep(10)

        upload_file = os.path.join(settings.MEDIA_ROOT, 'test.pdf')
        file_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        file_input.send_keys(upload_file)

        select_element = self.driver.find_element(By.NAME, 'student')
        select = Select(select_element)
        select.select_by_visible_text(name)

        elem = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        time.sleep(10)
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element(By.TAG_NAME, "p")
        self.assertIn("Here's your file :)", elem.text)
        elem = self.driver.find_element(By.LINK_TEXT, "open document")
        elem.send_keys(Keys.RETURN)

    def tearDown(self):
        time.sleep(10)
        self.driver.close()


