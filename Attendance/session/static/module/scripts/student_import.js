var metadata = [];
metadata.push({ name: "studentid", label: "Student Id", datatype: "string", editable: true });
metadata.push({ name: "firstname", label: "First Name", datatype: "string", editable: true });
metadata.push({ name: "lastname", label: "Last Name", datatype: "string", editable: true });

studentEditableGrid = new EditableGrid("StudentListTable");

$("#btn-preview-csv").click(function () {
    $('#file-student-csv').parse({
        config: {
            complete: function (results, file) {
                console.log("Parsing complete:", results, file);

                var namePolicyChoice = $('input[name=name-policies]:checked').val();
                var skipHeader = $('#skip-header').is(":checked");

                var studentCount = results.data.length;

                var colStudentId = $('#col-studentid').val();
                var colFirstname = $('#col-firstname').val();
                var colLastname = $('#col-lastname').val();
                var colFullname = $('#col-fullname').val();
                var numValidStudents = 0;

                var namePolicySeparate = function (row) {
                    return {
                        'firstname': row[colFirstname],
                        'lastname': row[colLastname]
                    };
                };
                var namePolicySingle = function (row) {
                    if (!row[colFullname]) return {};
                    var parts = row[colFullname].split(/[\s,]+/);
                    var lastnames = [];
                    var firstnames = [];
                    for (var i = 0; i < parts.length; i++) {
                        if (parts[i] === parts[i].toUpperCase())
                            lastnames.push(parts[i]);
                        else
                            firstnames.push(parts[i]);
                    }
                    return {
                        'firstname': firstnames.join(" "),
                        'lastname': lastnames.join(" ")
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
                    return str.charAt(0).toUpperCase() + str.toLowerCase().slice(1);
                }

                for (var i = skipHeader ? 1 : 0; i < studentCount; i++) {
                    var studentId = results.data[i][colStudentId];
                    if (!studentId) continue;

                    var student = namePolicy(results.data[i]);
                    if (!student['firstname'] || !student['lastname']) continue;

                    student['studentid'] = studentId;
                    student['firstname'] = toTitleCase(student['firstname']);
                    student['lastname'] = toTitleCase(student['lastname']);

                    data.push({ id: i, values: student });

                    ++numValidStudents;
                }

                $('#preview-message').text(`Found ${numValidStudents} records`);

                studentEditableGrid.load({ "metadata": metadata, "data": data });
                studentEditableGrid.renderGrid("student-list-preview", "table");
            }
        },
        before: function (file, inputElem) {
            $('#student-list-preview').empty();
        },
        error: function (err, file, inputElem, reason) {
            console.log(err);
        },
        complete: function () {

        }
    });
});