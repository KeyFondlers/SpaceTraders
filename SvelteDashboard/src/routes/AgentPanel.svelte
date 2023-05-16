<script>
    import * as AgentData from "../../../data/Agent.json"
</script>

<style>

    @font-face {
        font-family: "TrenchThin";
        src: local("TrenchThin"), url("../../fonts/TrenchThin.ttf") format("truetype");
    }

    .MainPanel {

        font-family: "TrenchThin";
        font-size: 25px;

        display: flex;
        flex-direction: column;
        align-items: left;
        justify-content: left;

        padding-left: 20px;
        padding-bottom: 0px;

        margin-top: 5px;
        margin-bottom: 5px;

        width: 500px;
        height: 175px;

        border-style: solid;
        border-width: 3px;
        border-color: orange;

    }
    
    .MainPanel > p{
        margin-top: 0px;
        margin-bottom: 0px;
    }

        
    .MainPanel > h1{
        margin-top: 5px;
        margin-bottom: 0px;
    }

</style>

<div class = "MainPanel">
    <h1>Agent Info</h1>
    <p>Name: {AgentData.data.symbol}</p>
    <p>ID: {AgentData.data.accountId}</p>
    <p>Headquarters: {AgentData.data.headquarters}</p>
    <p>Credit Balance: {AgentData.data.credits.toLocaleString()}</p>
</div>