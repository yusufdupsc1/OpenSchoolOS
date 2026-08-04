import type { Metadata } from "next";
import Link from "next/link";
import AuthHeader from "./AuthHeader";

export const metadata: Metadata = { title: "OpenSchoolOS" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-white text-neutral-900 antialiased">
        <header className="border-b">
          <nav className="mx-auto flex max-w-2xl items-center justify-between p-4 text-sm">
            <Link href="/" className="font-semibold">OpenSchoolOS</Link>
            <div className="flex items-center gap-4">
              <Link href="/" className="text-neutral-500 hover:underline">Students</Link>
              <Link href="/research" className="text-neutral-500 hover:underline">Research</Link>
              <AuthHeader />
            </div>
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
