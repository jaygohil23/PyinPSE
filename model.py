#For Meta model

metamodel_dict ={
    "nodes":[
        {
            "type": "Person",
            "edges":["Friends with","Child of","Parent of","Siblings of","Collegue of"]
        },
        {
            "type": "Pets",
            "edges":["Owned by","Friends with"]
        }
    ],

    "edges":["Friends with","Child of","Parent of","Siblings of","Collegue of"]
}