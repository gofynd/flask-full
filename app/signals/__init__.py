from blinker import signal


# mongoengine pre_update and post_update
me_pre_update = signal('me_pre_update')
me_post_update = signal('me_post_update')

#call external api pre and post signals
pre_call_api = signal('pre_call_api')
post_call_api = signal('post_call_api')