package org.openapitools.api;

import org.openapitools.model.User;
import org.openapitools.services.UserService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.context.request.NativeWebRequest;

import jakarta.validation.Valid;
import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("${openapi.userProduct.base-path:/api}")
public class UsersApiController implements UsersApi {

    private final NativeWebRequest request;
    private final UserService userService;

    @Autowired
    public UsersApiController(NativeWebRequest request, UserService userService) {
        this.request = request;
        this.userService = userService;
    }

    @Override
    public Optional<NativeWebRequest> getRequest() {
        return Optional.ofNullable(request);
    }

    // GET /users - Lấy tất cả users
    @Override
    public ResponseEntity<List<User>> usersGet() {
        List<User> users = userService.findAll();
        return ResponseEntity.ok(users);
    }

    // GET /users/{id} - Lấy user theo ID
    @Override
    public ResponseEntity<User> usersIdGet(String id) {
        Optional<User> user = userService.findById(id);
        return user.map(ResponseEntity::ok)
                   .orElse(ResponseEntity.notFound().build());
    }

    // POST /users - Tạo user mới
    @Override
    public ResponseEntity<Void> usersPost(@Valid @RequestBody User user) {
        userService.save(user);
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }

    // PUT /users/{id} - Cập nhật user
    @Override
    public ResponseEntity<Void> usersIdPut(String id, @Valid @RequestBody User user) {
        if (!userService.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        user.setId(id);
        userService.save(user);
        return ResponseEntity.ok().build();
    }

    // DELETE /users/{id} - Xóa user
    @Override
    public ResponseEntity<Void> usersIdDelete(String id) {
        if (!userService.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        userService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}