<script>

    var selectedContract = 0

    import * as Contracts from "../../../data/Contracts.json"


    /**
   * @param {string} date
   */
    function formatDate(date){
        const dateSec = Date.parse(date)
        const dateObj = new Date(dateSec)
        return dateObj.toLocaleTimeString() + " " + dateObj.toLocaleDateString()
    }

</script>


<div class = "ContractPanel">

    <h1>Contracts</h1>

    <p>Contract ID: {Contracts.data[selectedContract].id}</p>
    <p>Contract Type: {Contracts.data[selectedContract].type}</p>
    <p>Contract Terms: </p>
    <p style="text-indent: 20px;">Deadline: {formatDate(Contracts.data[selectedContract].terms.deadline)}</p>
    <p style="text-indent: 20px;">Upfront Payment: {Contracts.data[selectedContract].terms.payment.onAccepted.toLocaleString()} Credits</p>
    <p style="text-indent: 20px;">Delivery Payment: {Contracts.data[selectedContract].terms.payment.onFulfilled.toLocaleString()} Credits</p>
    <p>Contract Requirements: </p>
    <p style="text-indent: 20px;">Material: {Contracts.data[selectedContract].terms.deliver[0].tradeSymbol}</p>
</div>