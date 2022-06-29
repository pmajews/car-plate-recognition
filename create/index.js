const sql = require("mssql")

module.exports = async function (context, req) {
    try {
        var date = new Date();
        var currentDate = date.toISOString();
        await sql.connect(process.env.connectionString);
        const { plate } = req.body
        const result = await sql.query`insert into plates values(${currentDate},${plate})`
        context.res = {
            status: 200,
            headers:{ "Content-Type": "application/json"},
            body: "User successfully added",
        }
    } catch (err) {
    context.res = { status: 400, headers: { "Content-Type": "application/json", }, body: err, };
}
}