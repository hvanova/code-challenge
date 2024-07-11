import usaddress
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError


class Home(TemplateView):
    template_name = 'parserator_web/index.html'


class AddressParse(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        try: 
            address_string = request.query_params.get('address', '')
            if not address_string:
                raise ParseError("No address provided.")

            parsed_address = self.parse(address_string)
            return Response(
                {
                    "input_string": address_string, 
                    "address_components": parsed_address['address_components'], 
                    "address_type": parsed_address['address_type']
                    }
                )

        except Exception as e:
            return Response(
                {"error": "Could not parse address. Error: {}".format(str(e))},
                status=500
            )

    def parse(self, address):
        # using usaddress: https://github.com/datamade/usaddress
        tagged_address = usaddress.tag(address)
        address_components, address_type = tagged_address
        return {"address_components": address_components, "address_type": address_type}
