let schemaMeta = null;
let schemaFields = null;
let selectedModel = null;

// Returns an event handler that deletes the specified DOM element.
function deleteRow(row) {
    return function (e) {
        row.remove();
    }
}

// Returns an event handler that moves the specified DOM element towards the start of the list of child nodes.
function moveRowUp(row) {
    return function (e) {
        if (row.previousElementSibling) {
            row.parentNode.insertBefore(row, row.previousElementSibling);
        }
        e.target.blur()
    }
}

// Returns an event handler that moves the specified DOM element towards the end of the list of child nodes.
function moveRowDown(row) {
    return function (e) {
        if (row.nextElementSibling) {
            row.parentNode.insertBefore(row, row.nextElementSibling.nextElementSibling);
        }
        e.target.blur()
    }
}

// Creates an <option> element inside the specified parent element.
function createOption(parent, value, text) {
    const option = document.createElement("option");
    option.value = value;
    option.text = text;
    parent.appendChild(option);
    return option;
}

// Returns an event handler for when a (sub)field is selected in a field-row.
// The subsequent dropdowns on that row are deleted, and if the selected field has sub-fields,
// a single new dropdown is created for it.
function fieldSelectHandler(selectorContainer, selector, onChange) {
    return function (e) {
        while (selectorContainer.nextSibling) {
            selectorContainer.nextSibling.remove();
        }
        const selectedOption = selector.options[selector.selectedIndex];
        const selectedFieldType = selectedOption.dataset.fieldType;
        if (schemaFields.hasOwnProperty(selectedFieldType)) {
            createFieldSelect(selectorContainer.parentNode, selectedFieldType, onChange);
        }
        onChange(selector.dataset.modelName, selector.value);
    }
}

// Creates a dropdown inside the specified parent element, that selects fields from the specified model name.
// Selecting a field in the dropdown calls the function onChange(modelName, fieldName) where
// where modelName is the name of the model and fieldName is the name of the selected field within the model, or "" if no field is selected.
function createFieldSelect(parent, modelName, onChange) {
    const selectorContainer = document.createElement("div");
    parent.appendChild(selectorContainer);

    const selector = document.createElement("select");
    selector.className = 'field-select';
    selector.dataset.modelName = modelName;
    selector.addEventListener("change", fieldSelectHandler(selectorContainer, selector, onChange));
    selectorContainer.appendChild(selector);

    const defaultOption = createOption(selector, "", "Query " + schemaMeta[modelName].singular + "...");
    defaultOption.dataset.fieldType = "";
    defaultOption.selected = "selected";
    for (const fieldName in schemaFields[modelName]) {
        const field = schemaFields[modelName][fieldName];
        const newOption = createOption(selector, fieldName, field.label);
        newOption.dataset.fieldType = field.type;
    }
    selector.dataset.liveSearch = true;
    $(selector).selectpicker();
}

// Creates a <button> element inside the specified parent element.
function createButton(parent, className, text, action) {
    const button = document.createElement("button");
    button.className = className;
    button.addEventListener("click", action);
    button.appendChild(document.createTextNode(text));
    parent.appendChild(button);
}

// This is the event handler for the "Add Field" button.
function addFieldRow(e) {
    if (selectedModel === null) {
        return;
    }
    const fieldRow = document.createElement("div");
    fieldRow.className = "field-row";
    createButton(fieldRow, "btn btn-outline-danger", "X", deleteRow(fieldRow));
    createButton(fieldRow, "btn btn-outline-secondary", "\u25B2", moveRowUp(fieldRow));
    createButton(fieldRow, "btn btn-outline-secondary", "\u25BC", moveRowDown(fieldRow));
    createFieldSelect(fieldRow, selectedModel, function() {});
    document.getElementById("fieldRows").appendChild(fieldRow);
    e.target.blur();
}

function addFilterArgument(newFilter, argType) {
    let filterArgument;
    switch (argType) {
    case "string":
        filterArgument = document.createElement("input");
        filterArgument.type = "text";
        filterArgument.className = "form-control condition-argument";
        newFilter.appendChild(filterArgument);
        break;
    case "integer":
        filterArgument = document.createElement("input");
        filterArgument.type = "number";
        filterArgument.min = 0;
        filterArgument.value = 0;
        filterArgument.required = true;
        filterArgument.className = "form-control condition-argument";
        newFilter.appendChild(filterArgument);
        break;
    case "decimal":
        filterArgument = document.createElement("input");
        filterArgument.type = "number";
        filterArgument.min = 0;
        filterArgument.value = 0;
        filterArgument.step = "0.1";
        filterArgument.required = true;
        filterArgument.className = "form-control condition-argument";
        newFilter.appendChild(filterArgument);
        break;
    case "date":
        filterArgument = document.createElement("input");
        filterArgument.type = "date";
        filterArgument.value = new Date().toISOString().slice(0, 10);
        filterArgument.required = true;
        filterArgument.className = "form-control condition-argument";
        newFilter.appendChild(filterArgument);
        break;
    }
}

// Returns an event handler for selecting a filter condition from the (Add condition...) dropdown.
function addFilterCondition(filterContainer, selector) {
    return function (e) {
        if (selector.selectedIndex > 0) {
            const selectedOption = selector.options[selector.selectedIndex];
            const newFilter = document.createElement("div");
            newFilter.className = "filter-condition";

            const filterID = document.createElement("input");
            filterID.type = "hidden";
            filterID.className = "condition-id";
            filterID.value = selectedOption.value;

            const conjunctionText = document.createElement("span");
            conjunctionText.className = "conjunction";
            conjunctionText.appendChild(document.createTextNode("OR "));

            createButton(newFilter, "btn btn-outline-danger", "X", deleteRow(newFilter));
            newFilter.appendChild(filterID);
            newFilter.appendChild(conjunctionText);
            newFilter.appendChild(document.createTextNode(selectedOption.text));

            argTypeStr = selectedOption.dataset.argTypes;
            if (argTypeStr.length > 0) {
                for (argType of argTypeStr.split(" ")) {
                    addFilterArgument(newFilter, argType);
                }
            }

            filterContainer.appendChild(newFilter);
            selector.selectedIndex = 0;
            selector.blur();
        }
    }
}

// Returns an event handler for changing the field being filtered. The new field might be a different type
// and therefore require a different set of filters.
function changeFilterField(filterContainer, conditionSelector) {
    return function (modelName, fieldName) {
        const selectedField = schemaFields[modelName][fieldName];
        const selectedFieldType = fieldName === "" ? modelName : selectedField.type;
        filterContainer.innerHTML = "";
        conditionSelector.innerHTML = "";
        const firstOption = createOption(conditionSelector, "", "(Add condition...)");
        conditionSelector.selectedIndex = 0;
        let enableConditionSelector = true;

        switch (selectedFieldType) {
        case "string":
            createOption(conditionSelector, "iexact", "Equals (case insensitive)").dataset.argTypes = "string";
            createOption(conditionSelector, "icontains", "Contains").dataset.argTypes = "string";
            createOption(conditionSelector, "istartswith", "Starts with").dataset.argTypes = "string";
            createOption(conditionSelector, "iendswith", "Ends with").dataset.argTypes = "string";
            createOption(conditionSelector, "exact", "Equals (match case)").dataset.argTypes = "string";
            createOption(conditionSelector, "contains", "Contains (match case)").dataset.argTypes = "string";
            createOption(conditionSelector, "startswith", "Starts with (match case)").dataset.argTypes = "string";
            createOption(conditionSelector, "endswith", "Ends with (match case)").dataset.argTypes = "string";
            break;
        case "integer":
        case "decimal":
            createOption(conditionSelector, "exact", "Equals").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "gt", "Greater than").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "gte", "Greater or equal to").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "lt", "Less than").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "lte", "Less or equal to").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "range", "In range").dataset.argTypes = selectedFieldType + " " + selectedFieldType;
            break;
        case "date":
            createOption(conditionSelector, "exact", "Equals").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "gt", "After").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "gte", "On or after").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "lt", "Before").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "lte", "On or before").dataset.argTypes = selectedFieldType;
            createOption(conditionSelector, "range", "In range").dataset.argTypes = selectedFieldType + " " + selectedFieldType;
            break;
        case "enum":
            for (choice of selectedField.choices) {
                createOption(conditionSelector, choice[0], "= " + choice[1]).dataset.argTypes = "";
            }
            break;
        case "boolean":
            createOption(conditionSelector, "True", "= True").dataset.argTypes = "";
            createOption(conditionSelector, "False", "= False").dataset.argTypes = "";
            break;
        default:
            enableConditionSelector = false;
            break;
        }

        conditionSelector.style.display = enableConditionSelector ? null : "none";
    }
}

// This is the event handler for the "Add Filter" button.
function addFilterSection(e) {
    if (selectedModel === null) {
        return;
    }
    const filterSection = document.createElement("div");
    filterSection.className = "filter-section";

    const filterContainer = document.createElement("div");
    filterContainer.className = "filter-container bg-light";

    const conditionSelector = document.createElement("select");
    conditionSelector.className = "form-select";

    conditionSelector.addEventListener("change", addFilterCondition(filterContainer, conditionSelector));

    const fieldRow = document.createElement("div");
    fieldRow.className = "field-row";
    createButton(fieldRow, "btn btn-outline-danger", "X", deleteRow(filterSection));

    const conjunctionText = document.createElement("span");
    conjunctionText.className = "conjunction";
    conjunctionText.appendChild(document.createTextNode("AND"));
    fieldRow.appendChild(conjunctionText);

    const eventHandler = changeFilterField(filterContainer, conditionSelector);
    createFieldSelect(fieldRow, selectedModel, eventHandler);
    // Populate initial list of conditions
    eventHandler(selectedModel, "");

    filterSection.appendChild(fieldRow);
    filterSection.appendChild(filterContainer);
    filterSection.appendChild(conditionSelector);
    document.getElementById("filterSections").appendChild(filterSection);
    e.target.blur();
}

// Event handler for selecting / changing the starting table.
function selectStartingModel(e) {
    const startingTableSelector = document.getElementById("startingTableSelector");
    const selectedValue = startingTableSelector.value;
    if (selectedModel != selectedValue) {

        const fieldRows = document.getElementById("fieldRows");
        const filterSections = document.getElementById("filterSections");

        if (fieldRows.childNodes.length !== 0 || filterSections.childNodes.length !== 0) {
            if (!confirm("The current query will be erased if you change the starting table. Continue?")) {
                startingTableSelector.value = selectedModel;
                $(startingTableSelector).selectpicker("refresh");
                return;
            }
        }

        selectedModel = selectedValue;

        fieldRows.innerHTML = "";
        filterSections.innerHTML = "";
        document.getElementById("querySettings").style.display = selectedValue ? "block" : "none";
    }
}

// Given the DOM element for a field row (div.field-row), parse out the selected fields / subfields.
function parseFieldRow(row) {
    let fields = [];
    for (const field of row.querySelectorAll("select.field-select")) {
        if (field.value) {
            fields.push(field.value);
        }
    }
    return fields;
}

// Given the DOM element for a filter condition (div.filter-condition), parse out the id (e.g. "icontains") and the argument(s).
function parseFilterCondition(cond) {
    let filterArgs = [];
    for (const argField of cond.getElementsByClassName("condition-argument")) {
        filterArgs.push(argField.value);
    }
    return {
        id: cond.getElementsByClassName("condition-id")[0].value,
        args: filterArgs
    };
}

// Given the DOM element for a filter section (div.filter-section), parse out the fields being filtered, and the filter conditions.
function parseFilterSection(sect) {
    return {
        field: parseFieldRow(sect.getElementsByClassName("field-row")[0]),
        conditions: Array.from(sect.getElementsByClassName("filter-container")[0].getElementsByClassName("filter-condition"), parseFilterCondition)
    };
}

// Parse the entire contents of the query form into a JavaScript object.
function parseQuery() {
    return {
        startTable: selectedModel,
        fields: Array.from(document.getElementById("fieldRows").getElementsByClassName("field-row"), parseFieldRow),
        filters: Array.from(document.getElementById("filterSections").getElementsByClassName("filter-section"), parseFilterSection)
    };
}

function runQuery() {
    return fetch(dataLocation, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(parseQuery())
    })
    .then((responseObj) => responseObj.json())
}

function renderResultsTable(table, response) {
    table.innerHTML = "";
    const thead = document.createElement("thead");
    table.appendChild(thead);
    const tbody = document.createElement("tbody");
    table.appendChild(tbody);

    const headerRow = document.createElement("tr");
    thead.appendChild(headerRow);
    for (heading of response.headings) {
        const headingElement = document.createElement("th");
        headingElement.scope = "col";
        headingElement.appendChild(document.createTextNode(heading));
        headerRow.appendChild(headingElement);
    }
    for (row of response.data) {
        const rowElement = document.createElement("tr");
        for (cell of row) {
            const cellElement = document.createElement("td");
            cellText = (cell === null) ? "--" : cell;
            cellElement.appendChild(document.createTextNode(cellText));
            rowElement.appendChild(cellElement);
        }
        tbody.appendChild(rowElement);
    }
}

function quoteCSV(value) {
    if (value === null) {
        return "";
    }
    const escaped_str = String(value).replaceAll('"', '""');
    return `"${escaped_str}"`;
}

function exportResultsCSV(response) {
    csvHeaders = response.headings.map(quoteCSV).join(',')
    csvString = csvHeaders + '\r\n' + response.data.map((row) => {
        return row.map(quoteCSV).join(',')
    }).join('\r\n');
    const a = document.createElement('a');
    const blob = new Blob([csvString], {type: "data:text/csv;charset=utf-8,"});
    const url = URL.createObjectURL(blob);
    a.setAttribute('href', url);
    a.setAttribute('download', "query_results.csv");
    a.click();
    URL.revokeObjectURL(url);
}

window.addEventListener('load', (event) => {
    fetch(schemaLocation)
    .then((response) => response.json())
    .then((loadedSchema) => {
        schemaMeta = loadedSchema.meta;
        schemaFields = loadedSchema.fields;
        const startingTableSelector = document.getElementById("startingTableSelector");
        for (const model in schemaMeta) {
            if (!schemaMeta[model].fakeTable) {
                const option = createOption(startingTableSelector, model, schemaMeta[model].plural);
                option.dataset.tokens = model;
            }
        }
        startingTableSelector.addEventListener("change", selectStartingModel);
        $(startingTableSelector).selectpicker("refresh");
        document.getElementById("addFieldRow").addEventListener("click", addFieldRow);
        document.getElementById("addFilterSection").addEventListener("click", addFilterSection);
        document.getElementById("showResultsButton").addEventListener("click", (e) => {
            if (document.getElementById("querySettings").reportValidity()) {
                document.getElementById("queryResult").innerText = 'Loading...'
                runQuery()
                .then((response) => {
                    const table = document.getElementById("queryResult");
                    renderResultsTable(table, response);
                });
            }
        });
        document.getElementById("exportCSVButton").addEventListener("click", (e) => {
            if (document.getElementById("querySettings").reportValidity()) {
                runQuery().then(exportResultsCSV);
            }
        });
    });
});