import { useState } from "react";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Details from "./pages/Details";
import Chat from "./pages/Chat";
import Banks from "./pages/Banks";

function App() {
  const [page, setPage] = useState("landing");
  const [user, setUser] = useState(null);

  // Selected scheme banking information
  const [selectedBankData, setSelectedBankData] = useState(null);

  if (page === "landing") {
    return (
      <Landing
        user={user}
        onLogin={() => setPage("login")}
        onRegister={() => setPage("login")}
        onOpenSchemeAnalyzer={() => setPage("details")}
        onOpenBanks={() => setPage("banks")}
        onOpenChat={() => setPage("chat")}
        onLogout={() => setUser(null)}
      />
    );
  }

  if (page === "login") {
    return (
      <Login
        onLogin={() => {
          setUser({
            full_name: "Rajesh Kumar",
            category: "SC",
            state: "Uttar Pradesh",
            district: "Varanasi",
          });
          setPage("landing");
        }}
        onBack={() => setPage("landing")}
      />
    );
  }

  if (page === "details") {
    return (
      <Details
        onBack={() => setPage("landing")}
        onOpenChat={() => setPage("chat")}
        onOpenBanks={(data) => {
          setSelectedBankData(data);
          setPage("banks");
        }}
      />
    );
  }

  if (page === "chat") {
    return <Chat onBack={() => setPage("landing")} />;
  }

  if (page === "banks") {
    return (
      <Banks
        bankData={selectedBankData}
        onBack={() => setPage("landing")}
      />
    );
  }

  return null;
}

export default App;