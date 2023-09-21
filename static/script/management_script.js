document.addEventListener("DOMContentLoaded", function () {
    const userListState = document.getElementById("user-list-state");
    const monthListState = document.getElementById("month-list-state");
    const userSummaryState = document.getElementById("user-summary-state");
    const userList = document.getElementById("user-list");
    const monthList = document.getElementById("month-list");
    const userSummary = document.getElementById("user-summary");
    const recreateSummaryButton = document.getElementById("recreate-summary");

    fetch("/api/createSummary", {
        method: "POST"
    })
        .then(response => response.json())
        .then(data => {
            console.log("Summary creation result:", data);
        })
        .catch(error => {
            console.log("Error creating summary:", error);
        });

    function showUserListState() {
        userListState.style.display = "block";
        monthListState.style.display = "none";
        userSummaryState.style.display = "none";

        // Fetch user list from API and populate the user-list element
        fetch("/api/users")
            .then(response => response.json())
            .then(users => {
                userList.innerHTML = ""; // Clear existing list
                users.forEach(user => {
                    const li = document.createElement("li");
                    li.textContent = user.username;
                    li.addEventListener("click", function () {
                        showMonthListState(user.id);
                    });
                    userList.appendChild(li);
                });
            });
    }

    function showMonthListState(userId) {
        userListState.style.display = "none";
        monthListState.style.display = "block";
        userSummaryState.style.display = "none";

        // Fetch months from API and populate the month-list element
        fetch(`/api/user_summary_months?userId=${userId}`)
            .then(response => response.json())
            .then(data => {
                monthList.innerHTML = ""; // Clear existing list

                if (data.months) {
                    data.months.forEach(yearMonth => {
                        const formattedMonth = `${yearMonth.slice(0, 4)}年${yearMonth.slice(4)}月`;

                        const btn = document.createElement("button");
                        btn.textContent = formattedMonth;
                        btn.addEventListener("click", function () {
                            showUserSummaryState(userId, yearMonth);
                        });
                        monthList.appendChild(btn);
                    });
                } else {
                    monthList.innerHTML = "<p>No data available for this user.</p>";
                }
            })
            .catch(error => {
                console.error("Error fetching months:", error);
                monthList.innerHTML = "<p>Error loading data.</p>";
            });
    }

    function showUserSummaryState(userId, month) {
        userListState.style.display = "none";
        monthListState.style.display = "none";
        userSummaryState.style.display = "block";

        fetch(`/api/user_summary?userId=${userId}&month=${month}`)
            .then(response => response.json())
            .then(data => {
                userSummary.innerHTML = `
                    よく質問したこと: ${data.frequentQuestions} <br><br>
                    わからなかったこと: ${data.unresolvedIssues} <br><br>
                    チャット回数: ${data.chatCount}
                `;
            })
            .catch(error => {
                console.error("Error fetching user summary:", error);
                userSummary.innerHTML = "サマリ情報が取得できませんでした。";
            });

        recreateSummaryButton.addEventListener("click", function () {
            fetch(`/api/recreateSummary?userId=${userId}&month=${month}`, {
                method: "POST"
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("サマリを再作成しました。");
                        showUserSummaryState(userId, month);
                    } else {
                        alert("エラー：" + data.message);
                    }
                })
                .catch(error => {
                    alert("サマリの再作成に失敗しました。");
                });
        });
    }

    // Initialize with the user list state
    showUserListState();
});
