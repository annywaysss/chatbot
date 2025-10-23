import pathway as pw
class MySchema(pw.Schema):
    id: int
    name: str
data = pw.debug.table_from_rows(
    rows=[
        (1, "Ankita"),
        (2, "Rahul")
    ],
    schema=MySchema
)

pw.debug.compute_and_print(data)
pw.run()