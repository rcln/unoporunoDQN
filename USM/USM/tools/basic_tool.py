#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Josué Fabricio Urbina González"


class Utils:

    @staticmethod
    def get_query_param(src):

        id = src[0]
        attr = src[1]

        search = src[1]
        return id, attr, search
