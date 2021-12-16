#!/usr/bin/python3

import argparse, os, pyperclip
from common_res.dokuwiki_tools import DokuWikiPageWriter
from common_res.reddit_tools import RedditPost
from common_res.clc_tools import ColorPrint

def write_tree(writer, tree_root):
    writer.par(tree_root['content'])
    if 'responses' in tree_root:
        for tree_branch in tree_root['responses']:
            with writer.indented() as indent_env:
                with indent_env.collapsible(tree_branch['author']) as col_env:
                    write_tree(col_env, tree_branch)

def write_archive_article(writer, url):
    post = RedditPost(url)
    writer.title(post.tree['title'])
    writer.par('//{}//'.format(post.tree['author']))
    write_tree(writer, post.tree)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Archive a Reddit discussion as part of a DokuWiki page.')
    parser.add_argument('url_source', help='URL or text file with list of URL\'s')
    args = parser.parse_args()

    writer = DokuWikiPageWriter()
    writer.title_level -= 1

    if os.path.isfile(args.url_source):
        with open(args.url_source, 'r') as f:
            for line in f:
                write_archive_article(writer, line.strip())
    else:
        write_archive_article(writer, args.url_source)

    print(writer.toString())
    pyperclip.copy(writer.toString())
    ColorPrint.Green('Article text copied to clipboard.')

# ============================================

#!/usr/bin/python3
import sys, praw, os

reddit = praw.Reddit(
    user_agent='CMV Chapter Creation (by u/goromal)',
    client_id='e_Lf801LK7AtTA',
    client_secret='8tsv5GGTFJYI_-Ef50GWyJrdA5HXBw'
)

class RedditPost(object):
    def __init__(self, url, branching_factor=4, max_depth=4):
        self.submission = reddit.submission(url=url)
        title = self.submission.title
        author = self.submission.author.name
        description = self.submission.selftext

        self.tree = {'title': title, 'author': author, 'content': description}       
        self.populate_tree(self.tree, self.submission, self.expand_sub, 1, branching_factor, max_depth)
    
    def expand_sub(self, root):
        return sorted(root.comments, key=lambda x:x.score,reverse=True)

    def expand_com(self, root):
        return sorted(root.replies, key=lambda x:x.score,reverse=True)

    def populate_tree(self, tree_root, comment_root, expansion_fn, d, b, d_max):
        self.submission.comments.replace_more(limit=None)
        if d <= d_max:
            tree_root['responses'] = list()
            children = expansion_fn(comment_root)
            for i in range(min(b, len(children))):
                child = children[i]
                author = (child.author.name if not child.author is None else '')
                content = child.body
                tree_root['responses'].append({'title': '', 'author': author, 'content': content})
                self.populate_tree(tree_root['responses'][i], child, self.expand_com, d+1, b, d_max)
            
    def getTree(self):
        return self.tree