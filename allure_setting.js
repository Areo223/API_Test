// allure的配置文件

// 尝试从 localStorage 中获取 ALLURE_REPORT_SETTINGS 的值
let allureSettings = JSON.parse(localStorage.getItem('ALLURE_REPORT_SETTINGS'));
if (allureSettings) {
    // 如果能获取到值，则修改 language 属性为 "zh"
    allureSettings.language = "zh";
} else {
    // 如果获取不到值，则创建一个新对象并设置默认值
    allureSettings = {
        "language": "zh",
        "sidebarCollapsed": false,
        "sideBySidePosition": [46.83064516129034, 53.16935483870967]
    };
}
// 将修改后的对象或新创建的对象存储回 localStorage
localStorage.setItem('ALLURE_REPORT_SETTINGS', JSON.stringify(allureSettings));
console.log("当前设置", JSON.stringify(allureSettings));
