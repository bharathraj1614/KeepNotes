import "@/app/globals.css";
import ReduxProvider from "@/store/reduxprovider";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Keep Notes",
  description: "A simple notes taking app",
  other: {
    preconnect: ["https://fonts.googleapis.com", "https://fonts.gstatic.com"],
    stylesheet: [
      "https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap",
    ],
  },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <ReduxProvider>{children}</ReduxProvider>
      </body>
    </html>
  );
}
