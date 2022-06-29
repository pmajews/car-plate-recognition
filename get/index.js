const sql = require("mssql")

module.exports = async function (context, req) {
    try {
        await sql.connect(process.env.connectionString);
        const result = await sql.query`select * from plates`;
        context.res = {
            status: 200,
            headers: {
                "Content-Type": "application/json",
            },
            body: result.recordset,
        };
    } catch (err) {
        context.res = { status: 400, headers: { "Content-Type": "application/json", }, body: err, };
    }
}

