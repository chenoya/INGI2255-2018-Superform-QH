import os
import xml.etree.ElementTree as ET
from pathlib import Path

from superform import *
from superform.plugins import rss


def check_post(pub, path):
    tree = ET.parse(path)
    channel = tree.getroot().find('channel')
    last_item = channel.find('item')

    return last_item.find('title').text == pub.title and last_item.find('description').text == pub.description \
        and last_item.find('link').text == pub.link_url


def count(path):
    tree = ET.parse(path)
    root = tree.getroot()
    count1 = 0

    for _ in root.iter('item'):
        count1 += 1

    return count1


def del_file(path):
    for item in path:
        if Path(item).exists():
            os.remove(item)


def test_create_feed_if_none_exist():
    """
    Test if our module create a new RSS feed (new xml file) if it is the first time a post is send towards this channel.
    It also tests if it added the right post.
    """

    pub = Publishing(title="This is a test feed", description="This is a test description feed", link_url="www.facebook.com", channel_id=-1)

    path = "../plugins/rssfeeds/-1.xml"

    del_file([path])

    conf = "{\"feed_title\": \"-\", \"feed_description\": \"-\"}"

    rss.run(pub, conf)

    file = Path(path)

    assert file.exists()

    assert check_post(pub, path)

    del_file([path])


def test_different_channels():
    """
    Test if when publishing on different channels the posts are added to the right feed
    """

    pub1 = Publishing(title="first title", description="first description feed", link_url="www.google.com", channel_id=-2)
    pub2 = Publishing(title="second title", description="second description feed", link_url="www.google.com", channel_id=-3)

    conf1 = "{\"feed_title\": \"-\", \"feed_description\": \"-\"}"
    conf2 = "{\"feed_title\": \"-\", \"feed_description\": \"-\"}"

    path1 = '../plugins/rssfeeds/-2.xml'
    path2 = '../plugins/rssfeeds/-3.xml'

    del_file([path1, path2])

    rss.run(pub1, conf1)
    rss.run(pub2, conf2)

    assert Path(path1).exists()
    assert Path(path2).exists()

    assert count(path1) == 1
    assert count(path2) == 1

    assert check_post(pub1, path1)
    assert check_post(pub2, path2)

    del_file(['../plugins/rssfeeds/-2.xml', '../plugins/rssfeeds/-3.xml'])


def test_publish_post():
    """
    Test that when adding a new post to a feed it is actually added and added at the top of the feed
    """

    pub = Publishing(title="Voici un super beau titre", description="Avec une super description", link_url="www.facebook.com", date_from="2018-10-25", channel_id=-4)
    conf = "{\"feed_title\": \"-\", \"feed_description\": \"-\"}"

    path = "../plugins/rssfeeds/-4.xml"
    rss.run(pub, conf)

    count1 = count(path)

    rss.run(pub, conf)

    assert (count1 < count(path))
    assert check_post(pub, path)

    del_file([path])

