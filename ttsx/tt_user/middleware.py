class MyMidware(object):

    def process_view(self, request, view_name, view_args, view_kwargs):


            if request.path not in ['/user/register/',
                                '/user/register_handle/',
                                '/user/login/',
                                '/user/login_handle/',
                                '/user/logout/',
                                '/user/register_exist/',
                                '/user/order/','/user/info/','/user/site/','/user/active/','/user/pay/','/cart/add/'
                                '/cart/count/','/cart/delcart/','/cart/edit/'] :
                if not request.is_ajax():

                    request.session['url_path'] = request.get_full_path()





