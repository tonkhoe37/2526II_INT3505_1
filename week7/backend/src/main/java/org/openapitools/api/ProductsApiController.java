package org.openapitools.api;

import org.openapitools.model.Product;
import org.openapitools.services.ProductService;

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
public class ProductsApiController implements ProductsApi {

    private final NativeWebRequest request;
    private final ProductService productService;

    @Autowired
    public ProductsApiController(NativeWebRequest request, ProductService productService) {
        this.request = request;
        this.productService = productService;
    }

    @Override
    public Optional<NativeWebRequest> getRequest() {
        return Optional.ofNullable(request);
    }

    // GET /products
    @Override
    public ResponseEntity<List<Product>> productsGet() {
        return ResponseEntity.ok(productService.findAll());
    }

    // GET /products/{id}
    @Override
    public ResponseEntity<Product> productsIdGet(String id) {
        return productService.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    // POST /products
    @Override
    public ResponseEntity<Void> productsPost(@Valid @RequestBody Product product) {
        productService.save(product);
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }

    // PUT /products/{id}
    @Override
    public ResponseEntity<Void> productsIdPut(String id, @Valid @RequestBody Product product) {
        if (!productService.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        product.setId(id);
        productService.save(product);
        return ResponseEntity.ok().build();
    }

    // DELETE /products/{id}
    @Override
    public ResponseEntity<Void> productsIdDelete(String id) {
        if (!productService.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        productService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}