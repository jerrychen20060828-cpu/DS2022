// Step 2: select the bookstore database.
// At an interactive mongosh prompt, the equivalent command is: use bookstore
db = db.getSiblingDB("bookstore")

// Step 3: reload the starter authors.
db.authors.drop()
var authorsData = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(authorsData)

// Step 4: reload the starter books.
db.books.drop()
var booksData = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(booksData)

// Step 5: list every starter author and book.
print("Authors loaded from authors.json:")
db.authors.find().forEach(printjson)
print("Books loaded from books.json:")
db.books.find().forEach(printjson)

// Step 6: insert two additional books. Coraline uses an existing author;
// Kindred refers to the new author added in Step 7.
db.books.insertMany([
  {
    title: "Coraline",
    published_year: 2002,
    author_ids: ["author_002"]
  },
  {
    title: "Kindred",
    published_year: 1979,
    author_ids: ["author_004"]
  }
])

// Step 7: add the author needed by Kindred.
db.authors.insertOne({
  _id: "author_004",
  name: "Octavia E. Butler",
  nationality: "American",
  bio: {
    short: "American science-fiction author known for exploring power, identity, and inequality.",
    long: "Octavia E. Butler was an American science-fiction author whose influential novels include Kindred, Parable of the Sower, and the Patternist series. Her work frequently examines power, identity, community, and social inequality."
  }
})

// Step 8: find books by one starter author and the newly added author.
print("Books by Neil Gaiman or Octavia E. Butler:")
db.books.find({
  author_ids: { $in: ["author_002", "author_004"] }
}).forEach(printjson)
