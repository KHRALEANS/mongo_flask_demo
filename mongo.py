from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
import json


class JSONEncoder(json.JSONEncoder):
    # 将 bson 中的 ObjectId 类型编码为 json
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'platform'     # 设置 db 名称为 platform
app.config['MONGO_URI'] = 'mongodb://localhost:27017/platform'      # 设置连接字符串

mongo = PyMongo(app)

@app.route('/courses', methods=['GET'])
def get_all_courses():                      # 获取课程
    courses = mongo.db.courses              # 获取 courses 集合
    sorted_by = request.args.get('sort', default='id', type = str)  # 排序方式
    if sorted_by == 'likes':                # 根据点赞数排序
        q = list(courses.find().sort("likes", -1))
    elif sorted_by == 'id':                 # 根据课程 id 排序
        q = list(courses.find().sort("_id", 1))
    else:
        q = []
    res = json.dumps(q, cls=JSONEncoder)    # python list 编码为 json
    res = json.loads(res)                   # 加载 json 为 python list

    return jsonify({'result': res})         # 返回结果

@app.route('/courses', methods=['POST'])
def add_many_courses():                     # 批量添加课程到 courses
    courses = mongo.db.courses

    courses.insert_many(list(request.get_json()))

    return '',204

@app.route('/users', methods=['GET'])
def get_users():                            # 获取用户
    users = mongo.db.users                  # 获取 users 集合
    username = request.args.get('username', type = str)     # 查询用户名
    q = []
    if username:
        q = list(users.find({'username': username}))        # 根据用户名查询
    else:
        q = list(users.find())                              # 查询所有用户
    res = json.dumps(q, cls=JSONEncoder)
    res = json.loads(res)

    return jsonify({'result': res})

@app.route('/users', methods=['POST'])
def add_many_users():                       # 批量添加用户
    users = mongo.db.users

    users.insert_many(list(request.get_json()))

    return '',204

@app.route('/videos', methods=['GET'])
def get_all_videos():                       # 获取所有视频
    videos = mongo.db.videos

    q = list(videos.find())
    res = json.dumps(q, cls=JSONEncoder)
    res = json.loads(res)

    return jsonify({'result': res})

@app.route('/videos', methods=['POST'])
def add_many_videos():                      # 批量添加视频
    videos = mongo.db.videos

    videos.insert_many(list(request.get_json()))

    return '',204

@app.route('/user/<userid>/courses', methods=['GET'])
def get_user_courses(userid):               # 获取用户学习的课程
    users = mongo.db.users

    # 仅查询课程
    q = list(users.find({'_id': int(userid)}, {'courses': 1, '_id': 0}))
    res = json.dumps(q, cls=JSONEncoder)
    res = json.loads(res)

    return jsonify(res)

@app.route('/user/<userid>/videos', methods=['GET'])
def get_user_videos(userid):                # 获取用户观看的视频
    users = mongo.db.users
    unwatched = request.args.get('unwatched', default=0, type = int)    # 仅显示未完成观看

    pipeline = [
        {
            '$unwind': '$videos'            # 将文档中的嵌套数组的每个元素转为每一条文档
        },
        {
            '$match': {
                '_id': int(userid),         # 匹配 userid
                'videos.state': 0           # 匹配未完成观看状态
            }
        },
        {
            '$project': {
                'videos': 1,                # 仅保留 videos 字段
                '_id': 0                    # 去除 id 字段
            }
        }
    ]
    q = []
    if unwatched == 1:                      # 仅返回未完成视频
        q = list(users.aggregate(pipeline))
    else:                                   # 返回按视频 id 排序的视频
        q = list(users.find({'_id': int(userid)}, {'videos': 1, '_id': 0}))
    res = json.dumps(q, cls=JSONEncoder)
    res = json.loads(res)

    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)