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
                var skipHeader = $('#has-header').checked;

                var studentCount = results.data.length;
                var list = $('#student-list');

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
                var namePolicy = function () { }; // todo

                if (namePolicyChoice === 'separate') {
                    namePolicy = namePolicySeparate;
                }

                var data = [];

                for (var i = skipHeader ? 1 : 0; i < studentCount; i++) {
                    var studentId = results.data[i][colStudentId];
                    if (!studentId) continue;

                    ++numValidStudents;

                    var student = namePolicy(results.data[i]);
                    student['studentid'] = studentId;

                    data.push({ id: i, values: student });
                }

                $('#preview-message').text(`Found ${numValidStudents} records`);

                studentEditableGrid.load({ "metadata": metadata, "data": data });
                studentEditableGrid.renderGrid("student-list", "table");
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