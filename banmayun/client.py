from __future__ import absolute_import

import json
import re

from .rest import ErrorResponse


def format_path(path):
    if not path:
        return path

    path = re.sub(r'/+', '/', path)

    if path == '/':
        return ''
    else:
        return '/' + path.strip('/')


class BanmayunClient(object):
    def __init__(self, session):
        self.session = session
        self.rest_client = session.rest_client

    def get_session(self):
        return self.session

    def request(self, target, params=None):
        if params is None:
            params = {}

        base = self.session.build_url(target)
        headers, params = self.session.build_access_headers(base, params)

        url = self.session.build_url(target, params)
        return url, params, headers

    def get_current_user_id(self):
        return self.session.link["user_id"]

    def get_link(self, user_id, link_id):
        path = "/users/%s/links/%s" % (user_id, link_id)

        url, params, headers = self.request(path)
        return self.rest_client.GET(url, headers=headers)

    def list_links_for_user(self, user_id, offset=None, limit=None):
        path = "/users/%s/links" % user_id

        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def delete_link(self, user_id, link_id):
        path = "/users/%s/links/%s" % (user_id, link_id)

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def delete_links_for_user(self, user_id):
        path = "/users/%s/links" % user_id

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def exists_user(self, user):
        path = "/users/exists"

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(user))

    def create_user(self, user, password):
        path = "/users"
        params = {'password': password}

        url, params, headers = self.request(path, params=params)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(user))

    def get_user(self, user_id):
        path = "/users/%s" % user_id

        url, params, headers = self.request(path)
        return self.rest_client.GET(url, headers=headers)

    def list_users(self, role=None, is_activated=None, is_blocked=None, offset=None, limit=None):
        path = "/users"

        params = {}
        if role is not None:
            params['role'] = role
        if is_activated is not None:
            params['is_activated'] = is_activated
        if is_blocked is not None:
            params['is_blocked'] = is_blocked
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def update_user(self, user_id, update):
        path = "/users/%s/update" % user_id

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(update))

    def set_user_avatar(self, user_id, avatar_data):
        path = "/users/%s/avatar" % user_id

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/octet-stream'
        return self.rest_client.POST(url, headers=headers, body=avatar_data)

    def get_user_avatar(self, user_id, format_='png', size='m'):
        path = "/users/%s/avatar" % user_id
        params = {'format': format_,
                  'size': size}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def add_user_group(self, user_id, group_id, relation):
        path = "/users/%s/groups" % user_id
        params = {'group_id': group_id}

        url, params, headers = self.request(path, params=params)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(relation))

    def get_user_group(self, user_id, group_id):
        path = "/users/%s/groups/%s" % (user_id, group_id)

        url, params, headers = self.request(path)
        return self.rest_client.GET(url, headers=headers)

    def list_groups_for_user(self, user_id, role=None, is_activated=None, is_blocked=None, offset=None,
                             limit=None):
        path = "/users/%s/groups" % user_id

        params = {}
        if role is not None:
            params['role'] = role
        if is_activated is not None:
            params['is_activated'] = is_activated
        if is_blocked is not None:
            params['is_blocked'] = is_blocked
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def update_user_group(self, user_id, group_id, update):
        path = "/users/%s/groups/%s/update" % (user_id, group_id)

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(update))

    def remove_user_group(self, user_id, group_id):
        path = "/users/%s/groups/%s" % (user_id, group_id)

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def exists_group(self, group):
        path = "/groups/exists"

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(group))

    def create_group(self, group, owner_id=None):
        path = "/groups"

        params = {}
        if owner_id is not None:
            params['owner_id'] = owner_id

        url, params, headers = self.request(path, params=params)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(group))

    def get_group(self, group_id):
        path = "/groups/%s" % group_id

        url, params, headers = self.request(path)
        return self.rest_client.GET(url, headers=headers)

    def list_groups(self, type_=None, is_activated=None, is_blocked=None, offset=None, limit=None):
        path = "/groups"

        params = {}
        if type_ is not None:
            params['type'] = type_
        if is_activated is not None:
            params['is_activated'] = is_activated
        if is_blocked is not None:
            params['is_blocked'] = is_blocked
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def update_group(self, group_id, update):
        path = "/groups/%s" % group_id

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(update))

    def delete_group(self, group_id):
        path = "/groups/%s" % group_id

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def set_group_logo(self, group_id, logo_data):
        path = "/groups/%s/logo" % group_id

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/octet-stream'
        return self.rest_client.POST(url, headers=headers, body=logo_data)

    def get_group_logo(self, group_id, format_='png', size='m'):
        path = "/groups/%s/logo" % group_id
        params = {'format': format_,
                  'size': size}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def add_group_user(self, group_id, user_id, relation):
        path = "/groups/%s/users" % group_id
        params = {'user_id': user_id}

        url, params, headers = self.request(path, params=params)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(relation))

    def get_group_user(self, group_id, user_id):
        path = "/groups/%s/users/%s" % (group_id, user_id)

        url, params, headers = self.request(path)
        return self.rest_client.GET(url, headers=headers)

    def list_users_for_group(self, group_id, role=None, is_activated=None, is_blocked=None, offset=None,
                             limit=None):
        path = "/groups/%s/users" % group_id

        params = {}
        if role is not None:
            params['role'] = role
        if is_activated is not None:
            params['is_activated'] = is_activated
        if is_blocked is not None:
            params['is_blocked'] = is_blocked
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def update_group_user(self, group_id, user_id, update):
        path = "/groups/%s/users/%s/update" % (group_id, user_id)

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(update))

    def remove_group_user(self, group_id, user_id):
        path = "/groups/%s/users/%s" % (group_id, user_id)

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def get_root(self, root_id):
        path = "/roots/%s" % root_id

        url, params, headers = self.request(path)
        return self.rest_client.GET(url, headers=headers)

    def set_root_default_permission(self, root_id, default_permission):
        path = "/roots/%s/default_permission" % root_id

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(default_permission))

    def set_root_quota(self, root_id, quota):
        path = "/roots/%s/default_permission" % root_id

        params = {'quota': quota}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def put_file_by_path(self, root_id, full_path, file_obj, modified_at_millis, overwrite=False):
        path = "/roots/%s/files/p/%s" % (root_id, format_path(full_path))
        params = {'modified_at_millis': modified_at_millis,
                  'overwrite': overwrite}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.PUT(url, headers=headers, body=file_obj)

    def get_file_by_path(self, root_id, full_path, version=None, offset=None, bytes_=None):
        path = "/roots/%s/files/p/%s" % (root_id, format_path(full_path))

        params = {}
        if version is not None:
            params['version'] = version
        if offset is not None:
            params['offset'] = offset
        if bytes_ is not None:
            params['bytes'] = bytes_

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers, raw_response=True)

    def trash_file_by_path(self, root_id, full_path):
        path = "/roots/%s/files/p/%s" % (root_id, format_path(full_path))

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def upload_file(self, root_id, meta_id, file_obj, modified_at_millis):
        path = "/roots/%s/files/%s" % (root_id, meta_id)
        params = {'modified_at_millis': modified_at_millis}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers, body=file_obj)

    def get_file(self, root_id, meta_id, version=None, offset=None, bytes_=None):
        path = "/roots/%s/files/%s" % (root_id, meta_id)

        params = {}
        if version is not None:
            params['version'] = version
        if offset is not None:
            params['offset'] = offset
        if bytes_ is not None:
            params['bytes'] = bytes_

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers, raw_response=True)

    def trash_file(self, root_id, meta_id):
        path = "/roots/%s/files/%s" % (root_id, meta_id)

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers, raw_response=True)

    def get_file_thumbnail(self, root_id, meta_id, format_='png', size='m'):
        path = "/roots/%s/files/%s/thumbnail" % (root_id, meta_id)
        params = {'format': format_,
                  'size': size}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers, raw_response=True)

    def list_revisions_for_file(self, root_id, meta_id, offset=None, limit=None):
        path = "/roots/%s/files/%s" % (root_id, meta_id)

        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            limit['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def create_comment(self, root_id, meta_id, comment):
        path = "/roots/%s/files/%s/comments" % (root_id, meta_id)

        url, params, headers = self.request(path)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(comment))

    def get_comment(self, root_id, meta_id, comment_id):
        path = "/roots/%s/files/%s/comments/%s" % (root_id, meta_id, comment_id)

        url, params, headers = self.request(path)
        return self.rest_client.GET(url, headers=headers)

    def list_comments(self, offset=None, limit=None):
        path = "/roots/all/files/all/comments"

        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def list_comments_for_root(self, root_id, offset=None, limit=None):
        path = "/roots/%s/files/all/comments" % root_id

        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def list_comments_for_meta(self, root_id, meta_id, offset=None, limit=None):
        path = "/roots/%s/files/%s/comments" % (root_id, meta_id)

        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def delete_comment(self, root_id, meta_id, comment_id):
        path = "/roots/%s/files/%s/comments/%s" % (root_id, meta_id, comment_id)

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def delete_comments(self):
        path = "/roots/all/files/all/comments"

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def delete_comments_for_root(self, root_id):
        path = "/roots/all/files/%s/comments" % root_id

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def delete_comments_for_meta(self, root_id, meta_id):
        path = "/roots/%s/files/%s/comments" % (root_id, meta_id)

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def create_share(self, root_id, meta_id, share, password=None, expires_at_millis=None):
        path = "/roots/%s/files/%s/shares" % (root_id, meta_id)

        params = {}
        if password is not None:
            params['password'] = password
        if expires_at_millis is not None:
            params['expires_at_millis'] = expires_at_millis

        url, params, headers = self.request(path, params=params)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(share))

    def get_share(self, root_id, meta_id, share_id):
        path = "/roots/%s/files/%s/share/%s" % (root_id, meta_id, share_id)

        url, params, headers = self.request(path)
        return self.rest_client.GET(url, headers=headers)

    def list_shares(self, offset=None, limit=None):
        path = "/roots/all/files/all/shares"

        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def list_shares_for_root(self, root_id, offset=None, limit=None):
        path = "/roots/%s/files/all/shares" % root_id

        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def list_shares_for_meta(self, root_id, meta_id, offset=None, limit=None):
        path = "/roots/%s/files/%s/shares" % (root_id, meta_id)

        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def delete_share(self, root_id, meta_id, share_id):
        path = "/roots/%s/files/%s/shares/%s" % (root_id, meta_id, share_id)

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def delete_shares(self):
        path = "/roots/all/files/all/shares"

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def delete_shares_for_root(self, root_id):
        path = "/roots/all/files/%s/shares" % root_id

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def delete_shares_for_meta(self, root_id, meta_id):
        path = "/roots/%s/files/%s/shares" % (root_id, meta_id)

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def commit_chunked_upload(self, root_id, full_path, upload_id, modified_at_millis):
        path = "/fileops/commit_chunked_upload"
        params = {'root_id': root_id,
                  'path': format_path(full_path),
                  'upload_id': upload_id,
                  'modified_at_millis': modified_at_millis}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def copy_file(self, root_id, full_path, to_full_path):
        path = "/fileops/copy"
        params = {'root_id': root_id,
                  'path': format_path(full_path),
                  'to_path': format_path(to_full_path)}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def move_file(self, root_id, full_path, to_full_path):
        path = "/fileops/move"
        params = {'root_id': root_id,
                  'path': format_path(full_path),
                  'to_path': format_path(to_full_path)}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def create_folder(self, root_id, full_path, modified_at_millis=None):
        path = "/fileops/create_folder"
        params = {'root_id': root_id,
                  'path': format_path(full_path)}

        if modified_at_millis is not None:
            params['modified_at_millis'] = modified_at_millis

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def get_meta(self, root_id, full_path, list_=False):
        path = "/fileops/get_meta"
        params = {'root_id': root_id,
                  'path': format_path(full_path),
                  'list': list_}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def list_folder(self, root_id, full_path):
        path = "/fileops/list_folder"
        params = {'root_id': root_id,
                  'path': format_path(full_path)}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def rollback_file(self, root_id, full_path, to_version):
        path = "/fileops/rollback"
        params = {'root_id': root_id,
                  'path': format_path(full_path),
                  'to_version': to_version}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def thunder_upload(self, root_id, full_path, md5, bytes_, modified_at_millis):
        path = "/fileops/thunder_upload"
        params = {'root_id': root_id,
                  'path': format_path(full_path),
                  'md5': md5,
                  'bytes': bytes_,
                  'modified_at_millis': modified_at_millis}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def utime_folder(self, root_id, full_path, modified_at_millis):
        path = "/fileops/utime_folder"
        params = {'root_id': root_id,
                  'path': format_path(full_path),
                  'modified_at_millis': modified_at_millis}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def set_permission(self, root_id, full_path, permission):
        path = "/fileops/set_permission"
        params = {'root_id': root_id,
                  'path': format_path(full_path)}

        url, params, headers = self.request(path, params=params)
        headers['content-type'] = 'application/json'
        return self.rest_client.POST(url, headers=headers, body=json.dumps(permission))

    def list_permissions(self, root_id):
        path = "/fileops/list_permissions"
        params = {'root_id': root_id}

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def chunked_upload(self, file_obj, upload_id=None, offset=None):
        params = dict()

        if upload_id is not None:
            params['upload_id'] = upload_id
            params['offset'] = offset

        url, ignored_params, headers = self.request("/chunked_upload", params=params)

        # TODO:
        try:
            reply = self.rest_client.POST(url, headers=headers, body=file_obj)
            return reply['offset'], reply['upload_id']
        except ErrorResponse as e:
            raise e

    def delta(self, root_id, cursor_id=None):
        path = "/delta"
        params = {'root_id': root_id}

        if cursor_id is not None:
            params['cursor_id'] = cursor_id

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def get_trash(self, root_id, trash_id):
        path = "/roots/%s/trashes/%s" % (root_id, trash_id)

        url, params, headers = self.request(path)
        return self.rest_client.GET(url, headers=headers)

    def list_trashes_for_root(self, root_id,  offset=None, limit=None):
        path = "/roots/%s/trashes" % root_id

        params = {}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = offset

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def delete_trash(self, root_id, trash_id):
        path = "/roots/%s/trashes/%s" % (root_id, trash_id)

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def delete_trashes_for_root(self, root_id):
        path = "/roots/%s/trashes" % root_id

        url, params, headers = self.request(path)
        return self.rest_client.DELETE(url, headers=headers)

    def restore_trash(self, root_id, trash_id, to_full_path=None):
        path = "/roots/%s/trashes/%s/restore" % (root_id, trash_id)

        params = {}
        if to_full_path is not None:
            params['to_path'] = format_path(to_full_path)

        url, params, headers = self.request(path, params=params)
        return self.rest_client.POST(url, headers=headers)

    def search_users(self, query, group_id=None, offset=None, limit=None):
        path = "/search/users"

        params = {'query': query}
        if group_id is not None:
            params['group_id'] = group_id
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def search_groups(self, query, user_id=None, offset=None, limit=None):
        path = "/search/groups"

        params = {'query': query}
        if user_id is not None:
            params['user_id'] = user_id
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def search_files(self, query, root_id=None, full_path=None, offset=None, limit=None):
        path = "/search/files"

        params = {'query': query}
        if root_id is not None:
            params['root_id'] = root_id
        if path is not None:
            params['path'] = format_path(full_path)
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def top_users(self, order_by, offset=None, limit=None):
        path = "/top/users"

        params = {'order_by': order_by}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def top_groups(self, order_by, offset=None, limit=None):
        path = "/top/groups"

        params = {'order_by': order_by}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    def top_files(self, order_by, offset=None, limit=None):
        path = "/top/files"

        params = {'order_by': order_by}
        if offset is not None:
            params['offset'] = offset
        if limit is not None:
            params['limit'] = limit

        url, params, headers = self.request(path, params=params)
        return self.rest_client.GET(url, headers=headers)

    @staticmethod
    def __parse_meta_as_dict(raw_response):
        meta = None
        for header, header_val in raw_response.getheaders().iteritems():
            if header.lower() == 'x-banmayun-meta':
                try:
                    meta = json.loads(header_val)
                except ValueError:
                    raise ErrorResponse(raw_response, raw_response.read())
        if not meta:
            raise ErrorResponse(raw_response, raw_response.read())
        return meta
