% 1. 加载数据
% fort.1 包含三列：n, P, log(P) 
data = load('fort.1');

n = data(:, 1);
P = data(:, 2);
logP = data(:, 3);

% 2. 设置画布
fig = figure('Color', 'w', 'Position', [100, 100, 1200, 500]);

% --- 左图：概率分布 P(n) ---
subplot(1, 2, 1);
plot(n, P, 'Color', [0 0.4470 0.7410], 'LineWidth', 2);
hold on;
area(n, P, 'FaceColor', [0 0.4470 0.7410], 'FaceAlpha', 0.1); % 填充
title('Probability Distribution $P(n)$', 'Interpreter', 'latex', 'FontSize', 14);
xlabel('State $n$', 'Interpreter', 'latex');
ylabel('Probability $P$', 'Interpreter', 'latex');
grid on;

% --- 右图：对数概率 ln(P) 的二次特性 ---
subplot(1, 2, 2);
% 过滤掉 fort.1 中的 -Infinity 数据点 
validIdx = isfinite(logP); 
plot(n(validIdx), logP(validIdx), 'r.', 'MarkerSize', 10);
hold on;

% 进行二次多项式拟合以展示"二次分布"性质
p_coeff = polyfit(n(validIdx), logP(validIdx), 2);
n_fit = linspace(min(n(validIdx)), max(n(validIdx)), 100);
logP_fit = polyval(p_coeff, n_fit);
plot(n_fit, logP_fit, 'k--', 'LineWidth', 1.5);

title('Log-Probability $\ln(P)$ (Quadratic)', 'Interpreter', 'latex', 'FontSize', 14);
xlabel('State $n$', 'Interpreter', 'latex');
ylabel('$\ln(P)$', 'Interpreter', 'latex');
legend('Data from fort.1', 'Quadratic Fit', 'Location', 'southwest');
grid on;

% 3. 【新增】输出代码：保存为 JPG 文件
% 'DPI' 设置为 300 以保证学术报告所需的清晰度
exportgraphics(fig, 'distribution_plot.jpg', 'Resolution', 300);

fprintf('图像已成功保存至当前文件夹：distribution_plot.jpg\n');
fprintf('拟合方程参数: ln(P) = %.6f*n^2 + %.6f*n + %.6f\n', p_coeff);