from datetime import timedelta

from django.contrib import messages
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Emprestimo, Livro, Membro


def lista_livros(request):
    livros = Livro.objects.select_related("autor").order_by("titulo")
    membros = Membro.objects.order_by("nome")
    return render(request, "biblioteca/lista_livros.html", {
        "livros": livros,
        "membros": membros,
    })


@require_POST
def emprestar_livro(request, livro_id):
    with transaction.atomic():
        livro = get_object_or_404(Livro.objects.select_for_update(), pk=livro_id)

        if livro.copias_disponiveis <= 0:
            messages.error(request, f'Não há cópias disponíveis de "{livro.titulo}" no momento.')
            return redirect("lista_livros")

        membro = get_object_or_404(Membro, pk=request.POST.get("membro_id"))
        Emprestimo.objects.create(
            livro=livro,
            membro=membro,
            data_prevista_devolucao=timezone.localdate() + timedelta(days=14),
        )
        livro.copias_disponiveis -= 1
        livro.save(update_fields=["copias_disponiveis"])

    messages.success(request, f'Empréstimo de "{livro.titulo}" registrado com sucesso!')
    return redirect("lista_livros")


@require_POST
def devolver_livro(request, emprestimo_id):
    with transaction.atomic():
        emprestimo = get_object_or_404(
            Emprestimo.objects.select_related("livro", "membro").select_for_update(),
            pk=emprestimo_id,
        )

        if emprestimo.status == "DEVOLVIDO":
            messages.warning(request, "Este empréstimo já foi devolvido.")
            return redirect("meus_emprestimos", membro_id=emprestimo.membro_id)

        emprestimo.data_devolucao = timezone.localdate()
        emprestimo.status = "DEVOLVIDO"
        emprestimo.save(update_fields=["data_devolucao", "status"])

        livro = Livro.objects.select_for_update().get(pk=emprestimo.livro_id)
        livro.copias_disponiveis = min(livro.copias_disponiveis + 1, livro.copias_totais)
        livro.save(update_fields=["copias_disponiveis"])

    messages.success(request, f'Devolução de "{emprestimo.livro.titulo}" registrada.')
    return redirect("meus_emprestimos", membro_id=emprestimo.membro_id)


def meus_emprestimos(request, membro_id):
    membro = get_object_or_404(Membro, pk=membro_id)
    emprestimos = membro.emprestimo_set.select_related("livro").order_by("-data_emprestimo")
    return render(request, "biblioteca/meus_emprestimos.html", {
        "membro": membro,
        "emprestimos": emprestimos,
    })


def relatorio_livros(request):
    livros = Livro.objects.select_related("autor").annotate(
        total_emprestimos=Count("emprestimo")
    ).order_by("-total_emprestimos", "titulo")
    return render(request, "biblioteca/relatorio_livros.html", {"livros": livros})
