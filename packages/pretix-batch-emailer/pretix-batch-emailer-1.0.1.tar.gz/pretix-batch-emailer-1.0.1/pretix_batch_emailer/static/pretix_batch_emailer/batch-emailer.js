
$(document).ready(function () {
    const batch_emailer = function () {
        var orders = new Set();
        const regex = /(?<=\/orders\/)([A-Z\d]+)/;
        $('a').each(function () {
            const path = this.pathname;

            const o = path.match(regex);
            if (o !== null) {
                o.forEach(item => orders.add(item))
            }
        });
        console.log(orders);
        return (orders);
    };

    const fill_out_form = function () {
        const orders = batch_emailer()
        const url = window.location.href
        const orders_str = Array.from(orders).join(',')
        $('#batch_emailer_orders').val(orders_str)
        $('#batch_emailer_url').val(url);
        $('#batch_emailer').submit()

    }

    const match_url = window.location.href + "#batch-emailer";
    x = $('a[href*="#batch-emailer"]')

    console.log(x);
    x.click(fill_out_form)

});

