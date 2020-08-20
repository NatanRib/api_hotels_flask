from flask_restful import reqparse, Resource
from models.site_model import SiteModel
from flask_jwt_extended import jwt_required

body = reqparse.RequestParser()
body.add_argument('url', type=str, required=True, help= "The field 'url' cannot be left blank")

class Sites(Resource):

    def get(self):
        try:
            sites = SiteModel.all()
            return {'sites': [site.to_json() for site in sites]}, 200
        except:
            return {'mensage' : 'An error ocurred trying get the site.'}, 500

    @jwt_required
    def post(self):
        data = body.parse_args()
        site_exist = SiteModel.find_by_url(data.get('url'))
        if site_exist:
            return {'mensage' : "The site '{}' alread exist.".format(site_exist.url)}
       
        site = SiteModel(data['url'])
        try:
            site.save()
            return site.to_json(), 201
        except:
            return{'mensage': 'An error ocurred trying save the site.'}, 500

class Site(Resource):

    def get(self, site_url):
        try:
            site = SiteModel.find_by_url(site_url)
            if site:
                return site.to_json(), 200
            return {'mensage': 'the site {} not found'.format(site_url)}, 404
        except:
            return {'mensage': 'An error ocurred trying get the hotel.'}, 500

    @jwt_required
    def delete(self, site_url):
        site = SiteModel.find_by_url(site_url)
        if site:
            try:
                site.delete()
                return {'mensage':"The site {} as been deleted".format(site_url)}, 200
            except:
                return {'mensage':"An error ocurred trying delete the site {}".format(site_url)}, 500 
        return {'mensage':"The site {} not found".format(site_url)}, 404