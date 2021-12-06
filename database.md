### **Design of Database**
- Users：（用户表）
  - id
  - username
  - password
  - phone
  - address
  - state

<br>

- Courses：（课程表）
  - id
  - name
  - teacher
  - text(for 课程文本)
  - likes(for 点赞数)

<br>

- Videos: (视频表)
  - id
  - name(for 视频名称)
  - type(for 视频类型)
  - duration(for 持续时间)
  - path_to_store(for 存储路径)
  - added_date(for 添加日期)
  - updated_date(for 更新日期)
  - text(for 视频文本)

<br>

- UsersCourses：（用户课程表）
  - user_id(Reference:User.id)
  - course_id(Reference:Course.id)
  - learning_state（for 学习状态：正在学习，完成学习）
  - learning_progress (for 学习进度)
  - favourite(for 喜爱课程：喜爱，非喜爱)

<br>

- CoursesVideos: (课程-视频表)
  - course_id(Reference:Courses.id)
  - video_id(Reference:Videos.id)

<br>

- UsersVideos: (用户-视频表)
  - user_id(Reference:Users.id)
  - video_id(Reference:Videos.id)
  - offset(for 上次观看记忆时间)
  - state(for 观看状态：未看完，已看完)

<br>
