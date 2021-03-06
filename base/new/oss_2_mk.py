#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys

import oss2

PREFIX = 'http://peierlong-blog.oss-cn-hongkong.aliyuncs.com/'


def uploadToOSS(name, path):
    accessKeyId = "accessKeyId"
    accessKeySecret = "accessKeySecret"
    # endpoint = "oss-cn-qingdao-internal.aliyuncs.com"
    endpoint = "oss-cn-hongkong.aliyuncs.com"
    bucket = "peierlong-blog"
    auth = oss2.Auth(accessKeyId, accessKeySecret)
    service = oss2.Service(auth, endpoint)
    bucketObj = oss2.Bucket(auth, endpoint, bucket)
    bucketObj.put_object_from_file(name, path)


def getClipboardData():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    # 这里的data为bytes类型，之后需要转成utf-8操作
    return data


def setClipboardData(data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    p.communicate()


def main():
    if len(sys.argv) != 2:
        print("args error, ploease input the file path. ")

    path = sys.argv[1]
    obj_name = path[path.rfind("/") + 1:]

    print('obj_name : ' + obj_name)

    print('start upload to oss ....')
    uploadToOSS(obj_name, path)
    print('end upload to oss')

    mk_img = '![%s](%s)' % (obj_name, PREFIX + obj_name)
    setClipboardData(bytes(mk_img, 'utf8'))

    print('please CMD + v to paste markdown img grammar')


if __name__ == "__main__":
    main()
