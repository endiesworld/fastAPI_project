
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


all_posts = [{"title": "post_one", "content": "content for post one", "id": "1", "rating": 4},
             {"title": "post_two", "content": "content for post two", "id": "2", "rating": 3}]

def create_post(post):
    all_posts.append(post)
    return post


def get_one_post(id):
    post = [post for post in all_posts if post["id"] == id]
    if len(post) > 0:
        return post[0]
    return None


def delete_one_post(id):
    post_index = None
    deleted_post = None
    for index, post in enumerate(all_posts):
        if post["id"] == id:
            post_index = index
            deleted_post = post
            break
    if post_index is not None:
        all_posts.pop(post_index)
    return deleted_post


def update_one_post(post_id, update_post):
    post_index = None
    for index, post in enumerate(all_posts):
        if post["id"] == post_id:
            post_index = index
            break
    if post_index is not None:
        all_posts[post_index]["title"] = update_post["title"]
        all_posts[post_index]["content"] = update_post["content"]
        return all_posts[post_index]
    return None
