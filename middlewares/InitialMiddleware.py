
class InitialMiddleware(object):

    def process_request(self, request, spider):
        if 'retried_times' not in request.meta.keys():
            request.meta['retried_times'] = 0
        return None
