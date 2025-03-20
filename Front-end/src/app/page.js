"use client";
import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import { fetchNotes } from "@/store/notesSlice";
import Link from "next/link";

export default function Home() {
  const notes = useSelector((state) => state.notes.notes);
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadNotes = async () => {
      try {
        await dispatch(fetchNotes());
        setLoading(false);
      } catch (err) {
        setError("Error loading notes");
        setLoading(false);
      }
    };
    loadNotes();
  }, [dispatch]);

  if (loading) return <div>Loading notes...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div>
      <header>
        <nav>
          <ul>
            <li>
              <Link href="/">Home</Link>
            </li>
            <li>
              <Link href="/about">About</Link>
            </li>
            <li>
              <Link href="/account">Account</Link>
            </li>
            <li>
              <Link href="/logout">Logout</Link>
            </li>
          </ul>
        </nav>
        <h1>Good Morning Deva!</h1>
      </header>

      <main>
        <Link href="/create">
          <button>Add Notes</button>
        </Link>
        <ul className="home-notes-list">
          {notes &&
            notes.map((note) => (
              <li key={note.id} className="note-card">
                <Link href={`/notes/${note.id}`}>
                  <h2 className="note-title">{note.title}</h2>
                </Link>
              </li>
            ))}
        </ul>
      </main>
    </div>
  );
}
