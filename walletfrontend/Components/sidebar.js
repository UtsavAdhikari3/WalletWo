const { Component } = React;

class Sidebar extends Component {
  goToPage(link) {
    window.location.href = link;
  }

  render() {
    const { user, activePage } = this.props;

    const initials = user?.username
      ? user.username.slice(0, 2).toUpperCase()
      : "??";

    const mainLinks = [
      {
        icon: "🏠",
        label: "Dashboard",
        page: "dashboard",
        link: "../Dashboard/dashboard.html",
      },
      {
        icon: "💳",
        label: "My Wallet",
        page: "wallet",
        link: "../Dashboard/dashboard.html",
      },
      {
        icon: "↕️",
        label: "Transactions",
        page: "transactions",
        link: "../Transactions/transactions.html",
      },
      {
        icon: "📤",
        label: "Transfer",
        page: "transfer",
        link: "../Transfer/transfer.html",
      },
      {
        icon: "📥",
        label: "Deposit",
        page: "deposit",
        link: "../Deposit/deposit.html",
      },
    ];

    const accountLinks = [
      {
        icon: "⚙️",
        label: "Settings",
        page: "settings",
        link: "../Settings/settings.html",
      },
      {
        icon: "🔔",
        label: "Notifications",
        page: "notifications",
        link: "../Notifications/notifications.html",
      },
      {
        icon: "🛡️",
        label: "Security",
        page: "security",
        link: "../Security/security.html",
      },
    ];

    return (
      <div className="sidebar">
        <div
          className="sidebar-logo"
          onClick={() => this.goToPage("../Dashboard/dashboard.html")}
        >
          Wallet<span>Wo</span>
        </div>

        <div className="sidebar-section">Main</div>

        {mainLinks.map((item) => (
          <button
            key={item.label}
            className={`nav-item ${activePage === item.page ? "active" : ""}`}
            onClick={() => this.goToPage(item.link)}
          >
            <span className="ni-icon">{item.icon}</span>
            {item.label}
          </button>
        ))}

        <div className="sidebar-section">Account</div>

        {accountLinks.map((item) => (
          <button
            key={item.label}
            className={`nav-item ${activePage === item.page ? "active" : ""}`}
            onClick={() => this.goToPage(item.link)}
          >
            <span className="ni-icon">{item.icon}</span>
            {item.label}
          </button>
        ))}

        <div className="sidebar-bottom">
          <div className="user-chip">
            <div className="user-avatar">{initials}</div>
            <div className="user-info">
              <div className="user-name">{user?.username || "—"}</div>
              <div className="user-email">{user?.email || "—"}</div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
