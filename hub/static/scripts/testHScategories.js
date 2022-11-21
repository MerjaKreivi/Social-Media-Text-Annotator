// Meria's Annotator for Social Media Texts
// University of Oulu
// Created by Merja Kreivi-Kauppinen (2021-2022)

// Social-Media-Text-Annotator/HateSpeechAnnotator API testHScategories.js

// This file was created for testing purposes of HS categories

const HSCategoryLists = [["national", "immigration", "foreign", "ethnic", "religion"],
                        ["opinion", "politics", "status", "smedia", "work"],
                        ["sexual", "gender", "women", "health", "family"],
                        ["threat", "insult", "violence", "appearance", "joke"],
                        ["swear", "bully", "troll", "coded", "idiom"],
                        ["other"]];

function checkSelectedCategories(valueString) {	
    let valuelist = valueString.split(",");
    let cleanList = [];
    //let optionlist = [];
    let selectedDict = {};
    let categoryDictList = [];
    let i = 1;
    valuelist.forEach(element => 
    {    	
        let inLowerCase = element.toLowerCase().trim();        
        let input = `<label checked >${inLowerCase}</label>`;
        selectedDict[inLowerCase] = input;
        //optionlist.push(input);
        //cleanList.push(inLowerCase);
        i++;
    });
    console.log(selectedDict);
    
     HSCategoryLists.forEach(group => {
     		category = {};
        //console.log(group);
        group.forEach(item => {
        	category[item] = `<label>${item}</label>`;;                           	
        })
        categoryDictList.push(category);
     });
    console.log(categoryDictList);
           
		for(var key in selectedDict) {  	
        categoryDictList.forEach(catDict => 
        {
        	for (var catKey in catDict) {
          	if (catKey === key) {
            	catDict[catKey] = selectedDict[key];
              break;
            }
          }
        }
		)
            
      //var value = selectedDict[key];
			//newGrouplist.push(newGroup);  		
		}
    //console.log(categoryDictList);
    let selectionLists = [];
    categoryDictList.forEach(dict => {
    console.log(dict);
    	selectionList = [];
      for (const value of Object.values(dict)) {
      	console.log(value);
    		selectionList.push(value);
			}
      selectionLists.push(selectionList);
    });
    console.log(selectionLists);
    //console.log(newGrouplist);    
    /*for (var i = cleanList.length - 1; i >= 0; i--) {        
        newGroup = [];
        HSCategoryLists.forEach(group => {
            if (group.includes(cleanList[i])) {
                cleanList.splice(i, 1);
            }
        })        
    }*/

    /*i = 0;
    cleanList.forEach(item => {
        newGroup = [];        
        HSCategoryLists.forEach(group => {
            if (group.includes(item)) {
                const matchedItem = optionlist.splice(i);
                newGroup.push(matchedItem[0]);
            }            
        })
        i++;    
    });*/
    

}


checkSelectedCategories("opinion, immigration, status, smedia, idiom");

