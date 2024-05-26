#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Вариант 2.
Для индивидуального задания лабораторной работы 2.21
добавьте тесты с использованием модуля unittest,
проверяющие операции по работе с базой данных.
"""


import sqlite3
import unittest
from pathlib import Path

from students import add_student, create_db, select_all, select_students


class CreateDbTest(unittest.TestCase):
    def setUp(self):
        self.test_path = Path("db_test.db")

    def tearDown(self):
        self.test_path.unlink(missing_ok=True)

    def test_create_db(self):
        create_db(self.test_path)
        self.assertTrue(self.test_path.exists())

        conn = sqlite3.connect(self.test_path)
        cursor = conn.cursor()

        cursor.execute(
            """SELECT name FROM sqlite_master
            WHERE type='table' AND name='groups';"""
        )
        self.assertTrue(cursor.fetchone())

        cursor.execute("PRAGMA table_info(groups);")
        columns = cursor.fetchall()
        expected_columns = [
            (0, "group_id", "INTEGER", 0, None, 1),
            (1, "group_title", "TEXT", 1, None, 0),
        ]
        self.assertEqual(columns, expected_columns)

        cursor.execute(
            """SELECT name FROM sqlite_master
            WHERE type='table' AND name='students';"""
        )
        self.assertTrue(cursor.fetchone())

        cursor.execute("PRAGMA table_info(students);")
        columns = cursor.fetchall()
        expected_columns = [
            (0, "student_id", "INTEGER", 0, None, 1),
            (1, "student_name", "TEXT", 1, None, 0),
            (2, "group_id", "INTEGER", 1, None, 0),
            (3, "student_grades", "TEXT", 1, None, 0),
        ]
        self.assertEqual(columns, expected_columns)

        cursor.close()
        conn.close()


class TestStudents(unittest.TestCase):
    def setUp(self):
        self.test_db = Path("db_test.db")
        create_db(self.test_db)

    def tearDown(self):
        self.test_db.unlink(missing_ok=True)

    def test_add_student(self):
        add_student(self.test_db, "Захарова В.Г", "ЮРП-б-о-23-2", "4,5,5,4,5")
        add_student(self.test_db, "Волков О.Д", "ЭКМ-б-о-20-1", "5,5,5,4,5")

        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM groups")
        self.assertEqual(cursor.fetchone()[0], 2)

        cursor.execute("SELECT COUNT(*) FROM students")
        self.assertEqual(cursor.fetchone()[0], 2)

        cursor.execute(
            """
            SELECT students.student_name, groups.group_title,
            students.student_grades FROM students
            INNER JOIN groups ON groups.group_id = students.group_id
            """
        )
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        self.assertEqual(len(rows), 2)
        self.assertDictEqual(
            {
                "name": rows[0][0],
                "group": rows[0][1],
                "grades": rows[0][2],
            },
            {
                "name": "Захарова В.Г",
                "group": "ЮРП-б-о-23-2",
                "grades": "4,5,5,4,5",
            },
        )
        self.assertDictEqual(
            {
                "name": rows[1][0],
                "group": rows[1][1],
                "grades": rows[1][2],
            },
            {
                "name": "Волков О.Д",
                "group": "ЭКМ-б-о-20-1",
                "grades": "5,5,5,4,5",
            },
        )

    def test_select_all(self):
        add_student(self.test_db, "Захарова В.Г", "ЮРП-б-о-23-2", "4,5,5,4,5")
        add_student(self.test_db, "Волков О.Д", "ЭКМ-б-о-20-1", "5,5,5,4,5")

        students = select_all(self.test_db)
        self.assertEqual(len(students), 2)
        self.assertDictEqual(
            students[0],
            {
                "name": "Захарова В.Г",
                "group": "ЮРП-б-о-23-2",
                "grades": "4,5,5,4,5",
            },
        )
        self.assertDictEqual(
            students[1],
            {
                "name": "Волков О.Д",
                "group": "ЭКМ-б-о-20-1",
                "grades": "5,5,5,4,5",
            },
        )

    def test_select_students(self):
        add_student(self.test_db, "Васильева М.А", "ЭКМ-б-о-21-1", "5,5,3,4,5")
        add_student(self.test_db, "Захарова В.Г", "ЮРП-б-о-23-2", "4,5,5,4,5")
        add_student(self.test_db, "Волков О.Д", "ЭКМ-б-о-20-1", "5,5,5,4,5")

        students = select_students(self.test_db)
        self.assertEqual(len(students), 2)
        self.assertDictEqual(
            students[0],
            {
                "name": "Захарова В.Г",
                "group": "ЮРП-б-о-23-2",
                "grades": "4,5,5,4,5",
            },
        )
        self.assertDictEqual(
            students[1],
            {
                "name": "Волков О.Д",
                "group": "ЭКМ-б-о-20-1",
                "grades": "5,5,5,4,5",
            },
        )


if __name__ == "__main__":
    unittest.main()
