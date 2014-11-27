#!/usr/bin/env python

import json
import glob
import os
from flask import Flask, session, redirect, url_for, escape, request, jsonify, abort

DATA_DIR = "data/"

app = Flask(__name__)

config = json.loads(open("config.json","r").read())

class Item(object):
    def __init__(self, state, data):
        self.state = state
        self.data = data
    def __eq__(self, cmp_str):
        if self.data == cmp_str:
            return True
        else:
            return False
    def __str__(self):
        return "{} {}".format(self.state, self.data)
    def __repr__(self):
        return self.__str__()
    def set_checked(self):
        self.state = 'x'
    def set_unchecked(self):
        self.state = '-'
    def get_item(self):
        return [self.state, self.data]

class List(object):
    def __init__(self, data):
        self.items = []
        for d in data:
            d = d.strip().split(" ", 1)
            self.items.append(Item(d[0], d[1]))
    def __iter__(self):
        return iter(self.items)
    def __getitem__(self, item):
        idx = self.items.index(item)
        return self.items[idx]
    def add_item(self, item):
        if not item in self.items:
            self.items.append(Item("-", item))
    def delete_item(self, item):
        if item in self.items:
            self.items.pop(self.items.index(item))
    def get_checked(self):
        output = []
        for item in self.items:
            if item.state == 'x':
                output.append(item.data)
        return output
    def get_unchecked(self):
        output = []
        for item in self.items:
            if item.state == '-':
                output.append(item.data)
        return output
    def get_all(self):
        output = []
        for item in self.items:
            output.append(item.get_item())
        return output
    def human_readable(self):
        output = ""
        for d in self.items:
            output += "{}\n".format(d)
        return output

def read_list(list_name):
    try:
        data = open(DATA_DIR + list_name, 'r').readlines()
        return List(data)
    except:
        return None

def write_list(list_name, list_obj):
    try:
        open(DATA_DIR + list_name, 'w').writelines(list_obj.human_readable())
    except:
        pass

def authenticate(request):
    token = request.args.get('token')
    if config["tokens"].count(token) == 0:
        abort(401)

def lists():
    lists=glob.glob(DATA_DIR + "/*")
    lists = [os.path.basename(x) for x in lists]
    return lists


@app.route('/')
def index():
    return ""

@app.route('/lists')
def show_lists():
    authenticate(request)
    return jsonify(lists=lists())


@app.route('/lists/<list_name>')
def get_list(list_name):
    authenticate(request)
    data = read_list(list_name)
    return jsonify(ok=True, data=data.get_all())

@app.route('/lists/add', methods = ["GET", "POST"])
def add_list():
    authenticate(request)
    if request.method == "POST":
        list_name = request.form["list_name"]
        if not list_name in lists():
            write_list(list_name, List(""))
        return jsonify(ok=True)
    return '''
        <form action="" method="post">
            <p><input type=text name=list_name>
            <p><input type=submit value=add>
        </form>
        '''

@app.route('/lists/<list_name>/add', methods = ["GET", "POST"])
def add_to_list(list_name):
    authenticate(request)
    if request.method == "POST":
        items = read_list(list_name)
        items.add_item(request.form["item"])
        write_list(list_name, items)
        return jsonify(ok=True)
    return '''
        <form action="" method="post">
            <p><input type=text name=item>
            <p><input type=submit value=add>
        </form>
        '''

@app.route('/lists/<list_name>/done/<path:item>')
def complete_item(list_name, item):
    authenticate(request)
    items = read_list(list_name)
    if item in items:
        items[item].set_checked()
    write_list(list_name, items)
    return jsonify(ok=True, data=items.get_all())

@app.route('/lists/<list_name>/undone/<path:item>')
def ucomplete_item(list_name, item):
    authenticate(request)
    items = read_list(list_name)
    if item in items:
        items[item].set_unchecked()
    write_list(list_name, items)
    return jsonify(ok=True, data=items.get_all())

@app.route('/lists/<list_name>/delete/<path:item>')
def delete_item(list_name, item):
    authenticate(request)
    items = read_list(list_name)
    if item in items:
        items.delete_item(item)
    write_list(list_name, items)
    return jsonify(ok=True, data=items.get_all())



if __name__ == '__main__':
    app.secret_key = config["key"]
    app.debug = True
    app.run(host='0.0.0.0')
