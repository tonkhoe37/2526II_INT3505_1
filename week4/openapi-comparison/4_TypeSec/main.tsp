import "@typespec/http";

using Http;

model Book {
  id: string;
  title: string;
  author: string;
  price: float32;
}

model BookUpdate {
  title?: string;
  author?: string;
  price?: float32;
}

@route("/api/books")
namespace Books {
  @get op list(): Book[];

  @post op create(@body book: Book): Book;

  @get op get(@path id: string): Book;

  @put op update(@path id: string, @body book: BookUpdate): Book;

  @delete op delete(@path id: string): void;
}