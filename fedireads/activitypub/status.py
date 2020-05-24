''' status serializers '''
from uuid import uuid4

def get_rating_note(review):
    ''' simple rating, send it as a note not an artciel '''
    status = review.to_activity()
    status['content'] = 'Rated "%s": %d stars' % (
        review.book.title,
        review.rating,
    )
    status['type'] = 'Note'
    return status

def get_review_article(review):
    ''' a book review formatted for a non-fedireads isntance (mastodon) '''
    status = review.to_activity()
    if review.rating:
        status['name'] = 'Review of "%s" (%d stars): %s' % (
            review.book.title,
            review.rating,
            review.name
        )
    else:
        status['name'] = 'Review of "%s": %s' % (
            review.book.title,
            review.name
        )

    return status


def get_comment_article(comment):
    ''' a book comment formatted for a non-fedireads isntance (mastodon) '''
    status = comment.to_activity()
    status['content'] += '<br><br>(comment on <a href="%s">"%s"</a>)' % \
        (comment.book.local_id, comment.book.title)
    return status



def get_replies(status, replies):
    ''' collection of replies '''
    id_slug = status.remote_id + '/replies'
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': id_slug,
        'type': 'Collection',
        'first': {
            'id': '%s?page=true' % id_slug,
            'type': 'CollectionPage',
            'next': '%s?only_other_accounts=true&page=true' % id_slug,
            'partOf': id_slug,
            'items': [r.to_activity() for r in replies],
        }
    }


def get_replies_page(status, replies):
    ''' actual reply list content '''
    id_slug = status.remote_id + '/replies?page=true&only_other_accounts=true'
    items = []
    for reply in replies:
        if reply.user.local:
            items.append(reply.to_activity())
        else:
            items.append(reply.remote_id)
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': id_slug,
        'type': 'CollectionPage',
        'next': '%s&min_id=%d' % (id_slug, replies[len(replies) - 1].id),
        'partOf': status.remote_id + '/replies',
        'items': [items]
    }


def get_favorite(favorite):
    ''' like a post '''
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': favorite.remote_id,
        'type': 'Like',
        'actor': favorite.user.remote_id,
        'object': favorite.status.remote_id,
    }


def get_unfavorite(favorite):
    ''' like a post '''
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': '%s/undo' % favorite.remote_id,
        'type': 'Undo',
        'actor': favorite.user.remote_id,
        'object': {
            'id': favorite.remote_id,
            'type': 'Like',
            'actor': favorite.user.remote_id,
            'object': favorite.status.remote_id,
        }
    }


def get_boost(boost):
    ''' boost/announce a post '''
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': boost.remote_id,
        'type': 'Announce',
        'actor': boost.user.remote_id,
        'object': boost.boosted_status.remote_id,
    }


def get_add_tag(tag):
    ''' add activity for tagging a book '''
    uuid = uuid4()
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': str(uuid),
        'type': 'Add',
        'actor': tag.user.remote_id,
        'object': {
            'type': 'Tag',
            'id': tag.remote_id,
            'name': tag.name,
        },
        'target': {
            'type': 'Book',
            'id': tag.book.local_id,
        }
    }


def get_remove_tag(tag):
    ''' add activity for tagging a book '''
    uuid = uuid4()
    return {
        '@context': 'https://www.w3.org/ns/activitystreams',
        'id': str(uuid),
        'type': 'Remove',
        'actor': tag.user.remote_id,
        'object': {
            'type': 'Tag',
            'id': tag.remote_id,
            'name': tag.name,
        },
        'target': {
            'type': 'Book',
            'id': tag.book.local_id,
        }
    }
