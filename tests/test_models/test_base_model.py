#!/usr/bin/python3
""" Unittest for BaseModel class
"""

from datetime import datetime
import io
from os import path, remove
import unittest
from unittest.mock import patch
from time import sleep
from models.base_model import BaseModel, Base
from uuid import UUID
import json
import os

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'basemodel test not supported')
class test_basemodel(unittest.TestCase):
    """ test class for base_model class"""

    def __init__(self, *args, **kwargs):
        """ init the test class of basemodel"""
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ the set up method of the test class"""
        pass

    def tearDown(self):
        """the teardown method of the ctest class"""
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_init(self):
        """Tests the initialization of the model class.
        """
        self.assertIsInstance(self.value(), BaseModel)
        if self.value is not BaseModel:
            self.assertIsInstance(self.value(), Base)
        else:
            self.assertNotIsInstance(self.value(), Base)

    def test_default(self):
        """ default testing of basemodel"""
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ testing basemodel with kwargs"""
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ testing with kwargs again but with int kwargs"""
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save metthod"""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ testing the str method of themodel"""
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ testing the to_dict method"""
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)
        # Tests if it's a dictionary
        self.assertIsInstance(self.value().to_dict(), dict)
        # Tests if to_dict contains accurate keys
        self.assertIn('id', self.value().to_dict())
        self.assertIn('created_at', self.value().to_dict())
        self.assertIn('updated_at', self.value().to_dict())
        # Tests if to_dict contains added attributes
        mdl = self.value()
        mdl.firstname = 'Celestine'
        mdl.lastname = 'Akpanoko'
        self.assertIn('firstname', mdl.to_dict())
        self.assertIn('lastname', mdl.to_dict())
        self.assertIn('firstname', self.value(firstname='Celestine').to_dict())
        self.assertIn('lastname', self.value(lastname='Akpanoko').to_dict())
        # Tests to_dict datetime attributes if they are strings
        self.assertIsInstance(self.value().to_dict()['created_at'], str)
        self.assertIsInstance(self.value().to_dict()['updated_at'], str)
        # Tests to_dict output
        datetime_now = datetime.today()
        mdl = self.value()
        mdl.id = '012345'
        mdl.created_at = mdl.updated_at = datetime_now
        to_dict = {
            'id': '012345',
            '__class__': mdl.__class__.__name__,
            'created_at': datetime_now.isoformat(),
            'updated_at': datetime_now.isoformat()
        }
        self.assertDictEqual(mdl.to_dict(), to_dict)
        if os.getenv('HBNB_TYPE_STORAGE') != 'db':
            self.assertDictEqual(
                self.value(id='u-b34', age=13).to_dict(),
                {
                    '__class__': mdl.__class__.__name__,
                    'id': 'u-b34',
                    'age': 13
                }
            )
            self.assertDictEqual(
                self.value(id='u-b34', age=None).to_dict(),
                {
                    '__class__': mdl.__class__.__name__,
                    'id': 'u-b34',
                    'age': None
                }
            )
        # Tests to_dict output contradiction
        mdl_d = self.value()
        self.assertIn('__class__', self.value().to_dict())
        self.assertNotIn('__class__', self.value().__dict__)
        self.assertNotEqual(mdl_d.to_dict(), mdl_d.__dict__)
        self.assertNotEqual(
            mdl_d.to_dict()['__class__'],
            mdl_d.__class__
        )
        # Tests to_dict with arg
        with self.assertRaises(TypeError):
            self.value().to_dict(None)
        with self.assertRaises(TypeError):
            self.value().to_dict(self.value())
        with self.assertRaises(TypeError):
            self.value().to_dict(45)
        self.assertNotIn('_sa_instance_state', n)

    def test_kwargs_none(self):
        """ testing kwargs again with none"""
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ testing kwargs with one arg"""
        n = {'name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.name, n['name'])

    def test_id(self):
        """ testing id attr of the model"""
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ testing created at attr"""
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    def test_updated_at(self):
        """ testing updated at attr"""
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

class Test_init(unittest.TestCase):
    """ Class for unittest of __init__ """

    def setUp(self):
        """ Set up for all methods """
        pass

    def tearDown(self):
        """ Tear down for all methods """
        try:
            remove("file.json")
        except Exception:
            pass

    def test_instance_creation_no_arg(self):
        """ No arguments """
        b1 = BaseModel()
        self.assertTrue(hasattr(b1, "id"))
        self.assertTrue(hasattr(b1, "created_at"))
        self.assertTrue(hasattr(b1, "updated_at"))

    def test_attr_types(self):
        """ No arguments """
        b1 = BaseModel()
        self.assertEqual(type(b1.id), str)
        self.assertEqual(type(b1.created_at), datetime)
        self.assertEqual(type(b1.updated_at), datetime)

    def test_id_diff_for_each_instance(self):
        """ Checks If every id generated is different """
        b1 = BaseModel()
        b2 = BaseModel()
        b3 = BaseModel()
        b4 = BaseModel()
        self.assertFalse(b1.id == b2.id)
        self.assertFalse(b1.id == b3.id)
        self.assertFalse(b1.id == b4.id)
        self.assertFalse(b2.id == b3.id)
        self.assertFalse(b2.id == b4.id)
        self.assertFalse(b3.id == b4.id)

    " ===========================  ARGS  ================================"

    def test_args(self):
        """ Tests that args works """
        b1 = BaseModel(1)
        b2 = BaseModel(1, "hola")
        b3 = BaseModel(1, "hola", (1, 2))
        b4 = BaseModel(1, "hola", (1, 2), [1, 2])

    def test_args_def_(self):
        """ Tests that default attr are set even with args """
        b1 = BaseModel(1, "hola", (1, 2), [1, 2])
        self.assertTrue(hasattr(b1, "id"))
        self.assertTrue(hasattr(b1, "created_at"))
        self.assertTrue(hasattr(b1, "updated_at"))

    " =========================== KWARGS  =============================== "

    def test_instance_creation_kwarg(self):
        """ Arguments in Kwarg """
        d = {'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
             'created_at': '2017-09-28T21:03:54.053212',
             '__class__': 'BaseModel',
             'updated_at': '2017-09-28T21:03:54.056732'}
        b1 = BaseModel(**d)
        self.assertTrue(hasattr(b1, "id"))
        self.assertTrue(hasattr(b1, "created_at"))
        self.assertTrue(hasattr(b1, "updated_at"))
        self.assertTrue(hasattr(b1, "__class__"))
        self.assertTrue(b1.__class__ not in b1.__dict__)

        self.assertEqual(b1.id, '56d43177-cc5f-4d6c-a0c1-e167f8c27337')
        self.assertEqual(b1.created_at.isoformat(),
                         '2017-09-28T21:03:54.053212')
        self.assertEqual(b1.updated_at.isoformat(),
                         '2017-09-28T21:03:54.056732')

    def test_no_default_args(self):
        """ Checks if id and dates are created even if not in kwargs """
        d = {"name": "Holberton"}
        b1 = BaseModel(**d)
        self.assertTrue(hasattr(b1, "id"))
        self.assertTrue(hasattr(b1, "created_at"))
        self.assertTrue(hasattr(b1, "updated_at"))
        self.assertEqual(b1.name, "Holberton")

    def test_dates_str_to_datetime(self):
        """ Checks that the proper conversion is made for datetimes """

        d = {'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
             'created_at': '2017-09-28T21:03:54.053212',
             '__class__': 'BaseModel',
             'updated_at': '2017-09-28T21:03:54.056732'}
        b1 = BaseModel(**d)
        self.assertEqual(b1.created_at.isoformat(),
                         '2017-09-28T21:03:54.053212')
        self.assertEqual(b1.updated_at.isoformat(),
                         '2017-09-28T21:03:54.056732')
        self.assertEqual(type(b1.created_at), datetime)
        self.assertEqual(type(b1.updated_at), datetime)

    def test_args_kwargs(self):
        """ Tests that kwargs works even if there is args """

        d = {'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
             'created_at': '2017-09-28T21:03:54.053212',
             '__class__': 'BaseModel',
             'updated_at': '2017-09-28T21:03:54.056732'}
        b1 = BaseModel(1, "Hello", ["World"], **d)
        self.assertTrue(hasattr(b1, "id"))
        self.assertTrue(hasattr(b1, "created_at"))
        self.assertTrue(hasattr(b1, "updated_at"))
        self.assertTrue(hasattr(b1, "__class__"))
        self.assertTrue(b1.__class__ not in b1.__dict__)

        self.assertEqual(b1.id, '56d43177-cc5f-4d6c-a0c1-e167f8c27337')
        self.assertEqual(b1.created_at.isoformat(),
                         '2017-09-28T21:03:54.053212')
        self.assertEqual(b1.updated_at.isoformat(),
                         '2017-09-28T21:03:54.056732')


class Test_str__(unittest.TestCase):

    """ Class for testing __str__ method """

    def tearDown(self):
        """ Tear down for all methods """
        try:
            remove("file.json")
        except Exception:
            pass

    def test_print(self):
        """ Tests the __str__ method """
        b1 = BaseModel()
        s = "[{:s}] ({:s}) {:s}\n"
        s = s.format(b1.__class__.__name__, b1.id, str(b1.__dict__))
        with patch('sys.stdout', new=io.StringIO()) as p:
            print(b1)
            st = p.getvalue()
            self.assertEqual(st, s)

    def test_print2(self):
        """ Tests the __str__ method 2"""
        b1 = BaseModel()
        b1.name = "Holberton"
        b1.code = 123
        s = "[{:s}] ({:s}) {:s}\n"
        s = s.format(b1.__class__.__name__, b1.id, str(b1.__dict__))
        with patch('sys.stdout', new=io.StringIO()) as p:
            print(b1)
            st = p.getvalue()
            self.assertEqual(st, s)

    def test_print_args(self):
        """ Test __str__ with args """
        b1 = BaseModel(None, 1, ["A"])
        b1.name = "Holberton"
        b1.code = 123
        s = "[{:s}] ({:s}) {:s}\n"
        s = s.format(b1.__class__.__name__, b1.id, str(b1.__dict__))
        with patch('sys.stdout', new=io.StringIO()) as p:
            print(b1)
            st = p.getvalue()
            self.assertEqual(st, s)

    def test_print_kwargs(self):

        """ Test __str__ with prev set kwargs """
        d = {'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
             'created_at': '2017-09-28T21:03:54.053212',
             '__class__': 'BaseModel',
             'updated_at': '2017-09-28T21:03:54.056732'}
        b1 = BaseModel(**d)
        s = "[{:s}] ({:s}) {:s}\n"
        s = s.format(b1.__class__.__name__, b1.id, str(b1.__dict__))
        with patch('sys.stdout', new=io.StringIO()) as p:
            print(b1)
            st = p.getvalue()
            self.assertEqual(st, s)


class Test_save(unittest.TestCase):

    """ Class to test save method """

    def tearDown(self):
        """ Tear down for all methods """
        try:
            remove("file.json")
        except Exception:
            pass

    def test_save(self):
        """ Tests that update_at time is updated """

        b1 = BaseModel()
        crtime = b1.created_at
        uptime = b1.updated_at
        sleep(0.05)
        b1.save()
        self.assertFalse(uptime == b1.updated_at)
        self.assertTrue(crtime == b1.created_at)

    def test_type(self):
        """ Checks that after save updated_at type is datetime """

        b1 = BaseModel()
        b1.save()
        self.assertEqual(type(b1.updated_at), datetime)
        self.assertEqual(type(b1.created_at), datetime)


class Test_to_dict(unittest.TestCase):

    """ Class to test to_dict method """

    def tearDown(self):
        """ Tear down for all methods """
        try:
            remove("file.json")
        except Exception:
            pass

    def test_to_dict(self):
        """ Checks for correct dictionary conversion """
        b1 = BaseModel()
        b1.name = "Holberton"
        b1.code = 123
        d = {}
        d["id"] = b1.id
        d["created_at"] = b1.created_at.isoformat()
        d["updated_at"] = b1.updated_at.isoformat()
        d["name"] = b1.name
        d["code"] = b1.code

        dic = b1.to_dict()

        self.assertEqual(d["id"], dic["id"])
        self.assertEqual(d["created_at"], dic["created_at"])
        self.assertEqual(d["updated_at"], dic["updated_at"])
        self.assertEqual(d["name"], dic["name"])
        self.assertEqual(d["code"], dic["code"])

    def test_to_dict_class_dates(self):
        """ Checks for correct dictionary conversion """
        b1 = BaseModel()
        dic = b1.to_dict()
        self.assertEqual(dic["__class__"], "BaseModel")
        self.assertEqual(type(dic["created_at"]), str)
        self.assertEqual(type(dic["updated_at"]), str)

    def test_isoformat(self):
        """ Checks if date is converted to string in isoformat """
        b1 = BaseModel()
        ctime = datetime.now()
        uptime = datetime.now()
        b1.created_at = ctime
        b1.updated_at = uptime

        dic = b1.to_dict()
        self.assertEqual(dic["created_at"], ctime.isoformat())
        self.assertEqual(dic["updated_at"], uptime.isoformat())
