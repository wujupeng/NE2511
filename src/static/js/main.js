// 全局变量
const API_BASE_URL = '/api';
let currentUser = null;

// 初始化应用
async function initApp() {
    // 检查用户登录状态
    await checkAuthStatus();
    
    // 根据当前页面初始化对应功能
    const currentPath = window.location.pathname;
    if (currentPath.includes('/dashboard')) {
        initDashboard();
    } else if (currentPath.includes('/products')) {
        initProductsPage();
    } else if (currentPath.includes('/tracking')) {
        initTrackingPage();
    } else if (currentPath.includes('/quality')) {
        initQualityPage();
    } else if (currentPath.includes('/suppliers')) {
        initSuppliersPage();
    } else if (currentPath.includes('/devices')) {
        initDevicesPage();
    }
}

// 检查认证状态
async function checkAuthStatus() {
    try {
        const token = localStorage.getItem('access_token');
        if (!token) {
            redirectToLogin();
            return;
        }
        
        // 验证令牌（在实际应用中可以调用API验证）
        currentUser = JSON.parse(localStorage.getItem('user'));
        updateNavbarUserInfo();
    } catch (error) {
        console.error('认证检查失败:', error);
        logout();
    }
}

// 更新导航栏用户信息
function updateNavbarUserInfo() {
    const userInfoElement = document.querySelector('.navbar .user-info');
    if (userInfoElement && currentUser) {
        userInfoElement.innerHTML = `
            <span>欢迎, ${currentUser.username}</span>
            <button class="btn btn-secondary" onclick="logout()">登出</button>
        `;
    }
}

// 重定向到登录页
function redirectToLogin() {
    if (!window.location.pathname.includes('/login') && 
        !window.location.pathname.includes('/register')) {
        window.location.href = '/login';
    }
}

// 登出
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    currentUser = null;
    window.location.href = '/login';
}

// API请求封装
async function apiRequest(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = {
        'Content-Type': 'application/json'
    };
    
    const token = localStorage.getItem('access_token');
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const options = {
        method,
        headers
    };
    
    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `请求失败: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API请求错误:', error);
        showNotification('错误', error.message || '请求失败', 'error');
        throw error;
    }
}

// 显示通知
function showNotification(title, message, type = 'info') {
    // 简单的通知实现，实际应用中可以使用更复杂的通知库
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-title">${title}</div>
        <div class="notification-message">${message}</div>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#f8d7da' : type === 'success' ? '#d4edda' : '#cce5ff'};
        color: ${type === 'error' ? '#721c24' : type === 'success' ? '#155724' : '#004085'};
        padding: 15px;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        z-index: 1000;
        max-width: 300px;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transition = 'opacity 0.5s';
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 500);
    }, 3000);
}

// 显示加载状态
function showLoading(element) {
    const loadingHTML = `<div class="loading"></div>`;
    if (element) {
        element.innerHTML = loadingHTML;
    }
}

// 隐藏加载状态
function hideLoading(element) {
    if (element) {
        element.innerHTML = '';
    }
}

// 初始化仪表盘
async function initDashboard() {
    try {
        showLoading(document.getElementById('dashboard-stats'));
        const response = await apiRequest('/dashboard/stats');
        const stats = response.stats;
        
        renderDashboardStats(stats);
    } catch (error) {
        console.error('获取仪表盘数据失败:', error);
    } finally {
        hideLoading(document.getElementById('dashboard-stats'));
    }
}

// 渲染仪表盘统计
function renderDashboardStats(stats) {
    const statsContainer = document.getElementById('dashboard-stats');
    if (!statsContainer) return;
    
    // 渲染概览统计卡片
    const overviewHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📦</div>
                <div class="stat-value">${stats.overview.total_products}</div>
                <div class="stat-label">总产品数</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">✅</div>
                <div class="stat-value">${stats.quality.pass_rate.toFixed(1)}%</div>
                <div class="stat-label">合格率</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⚙️</div>
                <div class="stat-value">${stats.devices.active}</div>
                <div class="stat-label">活跃设备</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📊</div>
                <div class="stat-value">${stats.overview.total_tracking}</div>
                <div class="stat-label">追踪产品</div>
            </div>
        </div>
    `;
    
    // 渲染最近活动
    let recentActivitiesHTML = '<div class="card">';
    recentActivitiesHTML += '<div class="card-header"><h3 class="card-title">最近活动</h3></div>';
    recentActivitiesHTML += '<ul class="list-group">';
    
    stats.recent_activities.forEach(activity => {
        recentActivitiesHTML += `
            <li class="list-group-item">
                <div>${activity.product_name} (${activity.product_code})</div>
                <div>${activity.check_type} - ${activity.result}</div>
                <div class="text-sm text-gray-500">${new Date(activity.time).toLocaleString()}</div>
            </li>
        `;
    });
    
    recentActivitiesHTML += '</ul></div>';
    
    statsContainer.innerHTML = overviewHTML + recentActivitiesHTML;
}

// 初始化产品页面
async function initProductsPage() {
    try {
        await loadProducts();
        
        // 绑定搜索按钮事件
        const searchBtn = document.getElementById('search-products');
        if (searchBtn) {
            searchBtn.addEventListener('click', handleProductSearch);
        }
    } catch (error) {
        console.error('初始化产品页面失败:', error);
    }
}

// 加载产品列表
async function loadProducts() {
    try {
        const productTableBody = document.getElementById('product-table-body');
        showLoading(productTableBody);
        
        const response = await apiRequest('/products');
        const products = response.products;
        
        let html = '';
        products.forEach(product => {
            html += `
                <tr>
                    <td>${product.product_code}</td>
                    <td>${product.product_name}</td>
                    <td>${product.product_type}</td>
                    <td>${new Date(product.production_date).toLocaleDateString()}</td>
                    <td>
                        <span class="badge badge-${getStatusClass(product.status)}">
                            ${getStatusText(product.status)}
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-secondary btn-sm" onclick="viewProduct(${product.id})")>查看</button>
                        <button class="btn btn-primary btn-sm" onclick="editProduct(${product.id})")>编辑</button>
                    </td>
                </tr>
            `;
        });
        
        productTableBody.innerHTML = html || '<tr><td colspan="6" class="text-center">暂无产品数据</td></tr>';
    } catch (error) {
        console.error('加载产品失败:', error);
    }
}

// 获取状态样式类
function getStatusClass(status) {
    const statusClasses = {
        'produced': 'info',
        'shipped': 'warning',
        'sold': 'success',
        'recalled': 'danger'
    };
    return statusClasses[status] || 'secondary';
}

// 获取状态文本
function getStatusText(status) {
    const statusTexts = {
        'produced': '已生产',
        'shipped': '已发货',
        'sold': '已售出',
        'recalled': '已召回'
    };
    return statusTexts[status] || status;
}

// 处理产品搜索
async function handleProductSearch() {
    const keyword = document.getElementById('product-search-keyword').value;
    if (!keyword) return;
    
    try {
        const response = await apiRequest(`/products/search?keyword=${encodeURIComponent(keyword)}`);
        const products = response.products;
        
        // 更新表格数据
        const productTableBody = document.getElementById('product-table-body');
        let html = '';
        products.forEach(product => {
            // 复用之前的行模板
            html += `
                <tr>
                    <td>${product.product_code}</td>
                    <td>${product.product_name}</td>
                    <td>${product.product_type}</td>
                    <td>${new Date(product.production_date).toLocaleDateString()}</td>
                    <td>
                        <span class="badge badge-${getStatusClass(product.status)}">
                            ${getStatusText(product.status)}
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-secondary btn-sm" onclick="viewProduct(${product.id})")>查看</button>
                        <button class="btn btn-primary btn-sm" onclick="editProduct(${product.id})")>编辑</button>
                    </td>
                </tr>
            `;
        });
        
        productTableBody.innerHTML = html || '<tr><td colspan="6" class="text-center">没有找到匹配的产品</td></tr>';
    } catch (error) {
        console.error('搜索产品失败:', error);
    }
}

// 初始化追踪页面
async function initTrackingPage() {
    // 追踪页面初始化逻辑
    const scanBtn = document.getElementById('scan-qr-code');
    if (scanBtn) {
        scanBtn.addEventListener('click', handleQRCodeScan);
    }
}

// 处理二维码扫描
async function handleQRCodeScan() {
    const qrCodeInput = document.getElementById('qr-code-input');
    const qrCodeData = qrCodeInput ? qrCodeInput.value : null;
    
    if (!qrCodeData) {
        showNotification('错误', '请输入二维码数据', 'error');
        return;
    }
    
    try {
        const response = await apiRequest('/tracking/scan', 'POST', { qr_code: qrCodeData });
        
        // 显示扫描结果
        const resultContainer = document.getElementById('scan-result');
        if (resultContainer) {
            resultContainer.innerHTML = `
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">产品信息</h3>
                    </div>
                    <div class="card-body">
                        <p><strong>产品名称:</strong> ${response.product.product_name}</p>
                        <p><strong>产品编码:</strong> ${response.product.product_code}</p>
                        <p><strong>当前状态:</strong> ${getStatusText(response.tracking.current_status)}</p>
                        <p><strong>当前位置:</strong> ${response.tracking.current_location}</p>
                    </div>
                </div>
            `;
        }
        
        showNotification('成功', '扫描成功', 'success');
    } catch (error) {
        console.error('扫描失败:', error);
    }
}

// 其他页面初始化函数
async function initQualityPage() { /* 质量检查页面初始化 */ }
async function initSuppliersPage() { /* 供应商页面初始化 */ }
async function initDevicesPage() { /* 设备页面初始化 */ }

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initApp);