from unittest.mock import Mock, patch

import pytest
from django.contrib.auth.models import Group

from ninja_extra import APIController, NinjaExtraAPI, exceptions, route, router, testing
from ninja_extra.controllers import RouteContext, RouteFunction
from ninja_extra.controllers.base import MissingRouterDecoratorException
from ninja_extra.controllers.response import Detail, Id, Ok
from ninja_extra.controllers.router import ControllerRouter
from ninja_extra.permissions.common import AllowAny


class SomeController(APIController):
    pass


class SomeControllerWithInject(APIController):
    def __init__(self, a: str):
        pass


class SomeControllerWithRoute(APIController):
    @route.get("/example")
    def example(self):
        pass

    @route.get("/example/{ex_id}")
    def example2(self, ex_id: str):
        pass


@router("", tags=["new tag"])
class SomeControllerWithRouter(APIController):
    auto_import = False  # disable auto_import of the controller

    @route.get("/example")
    def example(self):
        pass

    @route.get("/example/{ex_id}")
    def example2(self, ex_id: str):
        return self.create_response(ex_id, status_code=302)

    @route.get("/example/{ex_id}/ok")
    def example_with_ok_response(self, ex_id: str):
        return self.Ok(ex_id)

    @route.get("/example/{ex_id}/id")
    def example_with_id_response(self, ex_id: str):
        return self.Id(ex_id)


class TestAPIController:
    def test_controller_should_have_preset_properties(self):
        api = NinjaExtraAPI()
        assert SomeController.tags == ["some"]
        assert SomeController._path_operations == {}
        assert SomeController.permission_classes == [AllowAny]
        assert SomeController._router is None
        assert SomeController.api is None
        assert SomeController.registered is False

        with pytest.raises(MissingRouterDecoratorException) as ex:
            api.register_controllers(SomeController)
        assert "Controller Router not found" in str(ex.value)

    def test_controller_with_router_should_have_preset_properties(self):
        api = NinjaExtraAPI()
        assert SomeControllerWithRouter.permission_classes == [AllowAny]
        assert isinstance(SomeControllerWithRouter._router, ControllerRouter)
        assert SomeControllerWithRouter.api is None
        assert SomeControllerWithRouter.registered is False

        api.register_controllers(SomeControllerWithRouter)
        assert SomeControllerWithRouter.api == api
        assert SomeControllerWithRouter.registered

    def test_controller_should_wrap_with_inject(self):
        assert not hasattr(SomeController.__init__, "__bindings__")
        assert hasattr(SomeControllerWithInject.__init__, "__bindings__")

    def test_controller_should_have_path_operation_list(self):
        assert len(SomeControllerWithRoute._path_operations) == 2

        route_function: RouteFunction = SomeControllerWithRoute.example
        path_view = SomeControllerWithRoute._path_operations.get(str(route_function))
        assert path_view, "route doesn't exist in controller"
        assert len(path_view.operations) == 1

        operation = path_view.operations[0]
        assert operation.methods == route_function.route.route_params.methods
        assert operation.operation_id == route_function.route.route_params.operation_id

    def test_controller_route_definition_should_return_instance_route_definitions(self):
        assert len(SomeControllerWithRoute._path_operations) == 2
        for route_definition in SomeControllerWithRoute.get_route_functions():
            assert isinstance(route_definition, RouteFunction)

    @pytest.mark.django_db
    def test_controller_get_object_or_exception_works(self):
        group_instance = Group.objects.create(name="_groupowner")

        controller_object = SomeController()
        context = RouteContext(request=Mock(), permission_classes=[AllowAny])
        controller_object.context = context
        with patch.object(
            AllowAny, "has_object_permission", return_value=True
        ) as c_cop:
            group = controller_object.get_object_or_exception(
                Group, id=group_instance.id
            )
            c_cop.assert_called()
            assert group == group_instance

        with pytest.raises(Exception) as ex:
            controller_object.get_object_or_exception(Group, id=1000)
            assert isinstance(ex, exceptions.NotFound)

        with pytest.raises(Exception) as ex:
            with patch.object(AllowAny, "has_object_permission", return_value=False):
                controller_object.get_object_or_exception(Group, id=group_instance.id)
                assert isinstance(ex, exceptions.PermissionDenied)

    @pytest.mark.django_db
    def test_controller_get_object_or_none_works(self):
        group_instance = Group.objects.create(name="_groupowner2")

        controller_object = SomeController()
        context = RouteContext(request=Mock(), permission_classes=[AllowAny])
        controller_object.context = context
        with patch.object(
            AllowAny, "has_object_permission", return_value=True
        ) as c_cop:
            group = controller_object.get_object_or_none(Group, id=group_instance.id)
            c_cop.assert_called()
            assert group == group_instance

        assert controller_object.get_object_or_none(Group, id=1000) is None

        with pytest.raises(Exception) as ex:
            with patch.object(AllowAny, "has_object_permission", return_value=False):
                controller_object.get_object_or_none(Group, id=group_instance.id)
                assert isinstance(ex, exceptions.PermissionDenied)


class TestAPIControllerResponse:
    ok_response = Ok("OK")
    id_response = Id("ID")
    detail_response = Detail(dict(errors=[dict(test="passed")]), status_code=302)

    def test_controller_response(self):
        # OK Response
        assert self.ok_response.get_schema() == Ok.get_schema()
        assert self.ok_response.convert_to_schema() == Ok.get_schema()(detail="OK")
        assert self.ok_response.status_code == Ok.status_code
        # ID Response
        assert self.id_response.get_schema() == Id.get_schema()
        assert self.id_response.convert_to_schema() == Id.get_schema()(id="ID")
        assert self.id_response.status_code == Id.status_code
        # Detail Response
        assert self.detail_response.get_schema() == Detail.get_schema()
        assert self.detail_response.convert_to_schema() == Detail.get_schema()(
            detail=dict(errors=[dict(test="passed")])
        )
        assert self.id_response.status_code != Detail.status_code

    def test_controller_response_works(self):
        detail = Detail("5242", status_code=302)
        client = testing.TestClient(SomeControllerWithRouter)
        response = client.get("/example/5242")

        assert response.status_code == 302
        assert detail.convert_to_schema().dict() == response.json()

        ok_response = Ok("5242")
        result = SomeControllerWithRouter.example_with_ok_response(
            request=Mock(), ex_id="5242"
        )
        assert isinstance(result, tuple)
        assert result[1] == ok_response.convert_to_schema()
        assert result[0] == ok_response.status_code

        id_response = Id("5242")
        result = SomeControllerWithRouter.example_with_id_response(
            request=Mock(), ex_id="5242"
        )
        assert isinstance(result, tuple)
        assert result[1] == id_response.convert_to_schema()
        assert result[0] == id_response.status_code
