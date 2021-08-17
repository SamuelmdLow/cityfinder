var selectionText = 0;

function displayTemp(type)
{
    if (type == "F")
    {
        document.getElementById("num1" + type).style.display = "block";
        document.getElementById("num2label" + type).innerHTML = "Highest (C°)";
        document.getElementById("num1label" + type).innerHTML = "Lowest (C°)";
    }
    else
    {
        document.getElementById("num1label" + type).innerHTML = "Ideal Temperature (C°)";
        document.getElementById("num2label" + type).innerHTML = "Weight per each Degree";
    }
}

function displayPop(type)
{
    if (type == "F")
    {
        document.getElementById("num1" + type).style.display = "block";
        document.getElementById("num2label" + type).innerHTML = "Highest";
        document.getElementById("num1label" + type).innerHTML = "Lowest";
    }
    else
    {
        document.getElementById("num1label" + type).innerHTML = "Ideal Population";
        document.getElementById("num2label" + type).innerHTML = "Weight per each Person";
    }
}

function displayUni(type)
{
    if (type == "F")
    {
        document.getElementById("num1" + type).style.display = "none";
        document.getElementById("num1" + type).value = 0;
        document.getElementById("num2label" + type).innerHTML = "Lowest Acceptable Rank";
        document.getElementById("num1label" + type).innerHTML = "";
    }
    else
    {
        document.getElementById("num1label" + type).innerHTML = "Ideal University Rank";
        document.getElementById("num2label" + type).innerHTML = "Weight per each Rank";
    }
}

function updateSelection(type)
{
    var selection =  document.getElementsByName("selection" + type);

    if (selection[0].checked == true)
    {
        displayTemp(type);
        selectionText = "LT";
    }
    else if (selection[1].checked == true)
    {
        displayTemp(type);
        selectionText = "HT";
    }
    else if (selection[2].checked == true)
    {
        displayTemp(type);
        selectionText = "AT";
    }
    else if (selection[3].checked == true)
    {
        displayPop(type);
        selectionText = "PP";
    }
    else if (selection[4].checked == true)
    {
        displayUni(type);
        selectionText = "UR";
    }
}

function updatePage1(type)
{
    document.getElementById('form' + type).style.display = 'none';

    var URL = window.location.href;

    URL = URL.split("/");
    URL = URL[URL.length - 1];

    if (URL != "0")
    {
        if (URL.includes("::"))
        {
            URL = URL.split("::")
            RCODE = URL[0];
            FCODE = URL[1];
        }
        else if (URL.includes("RNK:"))
        {
            RCODE = URL.slice(4, URL.length);
            FCODE = "";
        }
        else if (URL.includes("FLT:"))
        {
            RCODE = "";
            FCODE = URL.slice(4, URL.length);
        }
    }
    else
    {
        RCODE = "";
        FCODE = "";
    }

    updatePage2(type, RCODE, FCODE);
}

function updatePage2(type, RCODE, FCODE)
{
    if (type == "R")
    {
        RCODE = NewCode(RCODE, type);
        if (RCODE != "ERROR")
        {
            if (FCODE.length == 0)
            {
                window.location.replace('/filter/RNK:' + RCODE);
            }
            else
            {
                window.location.replace('/filter/' + RCODE + "::" + FCODE);
            }
        }
    }
    else
    {
        FCODE = NewCode(FCODE, type);
        if (FCODE != "ERROR")
        {
            if (RCODE.length == 0)
            {
                window.location.replace('/filter/FLT:' + FCODE);
            }
            else
            {
                window.location.replace('/filter/' + RCODE + "::" + FCODE);
            }
        }
    }
}


function NewCode(CODE, type)
{
    var NEWCODE = "";
    if (CODE.includes(selectionText) == true)
    {
        var NEWCODE = "";
        var RAWFILTERS  = CODE.split(":");
        var FILTERS     = [];
        for (let i = 0; i < RAWFILTERS.length; i++)
        {
            if (RAWFILTERS[i].includes(selectionText) != true)
            {
                NEWCODE = NEWCODE + RAWFILTERS[i] + ":";
            }
        }
    }
    else
    {
        if (CODE != "")
        {
            NEWCODE = CODE + ":";
        }
    }

    var NUM1 = document.getElementById("num1" + type).value;
    var NUM2 = document.getElementById("num2" + type).value;

    if (NUM1 == "")
    {
        NUM1     = 1;
    }
    if (NUM2 == "")
    {
        NUM2    = 1;
    }

    if (parseInt(NUM1) > parseInt(NUM2) && type == "F")
    {
        alert("The Lower bound (" + String(NUM1) +") cannot be higher than the Upper Bound(" + String(NUM2) +")!");
        return "ERROR";
    }
    else if (selectionText == 0)
    {
        alert("Please select a filter!");
        return "ERROR";
    }
    else
    {
        NUM1 = String(NUM1);
        NUM2 = String(NUM2);
        NEWCODE = NEWCODE + selectionText + NUM1 + "_" + NUM2;
        return NEWCODE;
    }
}

function reset()
{
    window.location.replace('/');
}