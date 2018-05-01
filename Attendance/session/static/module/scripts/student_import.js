var preview_table = function () {
    $('#file-student-csv').parse({
        config: {
            complete: function (results, file) {
                console.log("Parsing complete:", results, file);

                var namePolicyChoice = import_app.name_policy_choice;
                var skipHeader = import_app.skip_header;

                var studentCount = results.data.length;

                var colStudentId = import_app.col_student_id;
                var colFirstname = import_app.col_first_name;
                var colLastname = import_app.col_last_name
                var colFullname = import_app.col_full_name;
                var numValidStudents = 0;

                var namePolicySeparate = function (row) {
                    return {
                        'First Name': row[colFirstname],
                        'Last Name': row[colLastname]
                    };
                };
                // todo: corner cases - single letter name parts, mixed cases (e.g. "HELLO Im TOUGH")
                var namePolicySingle = function (row) {
                    if (!row[colFullname]) return {};
                    var parts = row[colFullname].split(/[\s,]+/);
                    var lastnames = [];
                    var firstnames = [];
                    for (var i = 0; i < parts.length; i++) {
                        if (!parts[i]) continue;
                        if (parts[i] === parts[i].toUpperCase())
                            lastnames.push(parts[i]);
                        else
                            firstnames.push(parts[i]);
                    }
                    return {
                        'First Name': firstnames.join(" "),
                        'Last Name': lastnames.join(" ")
                    };
                };
                var namePolicy = function () { };

                if (namePolicyChoice === 'separate') {
                    namePolicy = namePolicySeparate;
                } else if(namePolicyChoice === 'single') {
                    namePolicy = namePolicySingle;
                }

                var data = [];

                var toTitleCase = function(str) {
                    return str[0].toUpperCase() + str.slice(1).toLowerCase();
                }

                for (var i = skipHeader ? 1 : 0; i < studentCount; i++) {
                    var studentId = results.data[i][colStudentId];
                    if (!studentId) continue;

                    var student = namePolicy(results.data[i]);
                    if (!student['First Name'] || !student['Last Name']) continue;

                    student['Student Id'] = studentId;
                    student['First Name'] = toTitleCase(student['First Name']);
                    student['Last Name'] = toTitleCase(student['Last Name']);

                    data.push(student);

                    ++numValidStudents;
                }

                $('#preview-message').text(`Found ${numValidStudents} records`);
                $("#student-list-preview").jsGrid({
                    inserting: true,
                    editing: true,

                    width: "100%",

                    noDataContent: "No Record",

                    data: data,
                    fields: [
                        { name: "Student Id", type: "text", validate: "required" },
                        { name: "First Name", type: "text", validate: "required" },
                        { name: "Last Name", type: "text", validate: "required" },
                        { type: "control" }
                    ]
                });

            }
        },
        before: function (file, inputElem) {
            // $('#student-list-preview').empty();
        },
        error: function (err, file, inputElem, reason) {
            console.log(err);
        },
        complete: function () {

        }
    });
};

var upload_list = function() {
    var tableData = $('#student-list-preview').data('JSGrid').data;
    var csvString = "";
    for (var i = 0; i < tableData.length; ++i) {
        csvString += `${tableData[i]['Student Id']},${tableData[i]['First Name']},${tableData[i]['Last Name']}\n`;
    }

    var csvFormData = new FormData();
    var csvBlob = new Blob([csvString], { type: 'text/csv' });

    csvFormData.set('student_list_csv', csvBlob, 'students.csv');
    csvFormData.set('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val());

    var request = new XMLHttpRequest();
    request.open('POST', postUrl);
    request.send(csvFormData);

    // todo: reload after POST success, or display conflict list
};

var import_app = new Vue({
    el: '#import_app',
    data: {
        step: 0,
        file: null,
        col_student_id: null,
        col_first_name: null,
        col_last_name: null,
        col_full_name: null,
        name_policy_choice: 'separate',
        skip_header: true
    },
    methods: {
        select_fields() {
            if(!this.file) alert("You must select a file to proceed!");
            else this.step = 2;
        },
        preview() {
            this.step = 3;
            preview_table();
        },
        upload() {
            upload_list();
        }
    }
});
